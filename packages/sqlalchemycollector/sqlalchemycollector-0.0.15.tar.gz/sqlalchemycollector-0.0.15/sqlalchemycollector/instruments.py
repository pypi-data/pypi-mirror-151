from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime
import json
import os
import typing
import uuid

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import ReadableSpan, Status, StatusCode, TracerProvider
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SpanExportResult,
    SimpleSpanProcessor,
)
from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from sqlalchemy.event import listen
from sqlalchemycollector.plan_collect_type import PlanCollectType


METIS_DO_NOT_TRACK_COMMENT = "/*METIS_DO_NOT_TRACK*/"

FILE_NAME = "metis-log-collector.log"

METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER = "track.by.metis"
METIS_PLAN_SPAN_ATTRIBUTE = "metis.statement.plan"
METIS_STATEMENT_SPAN_ATTRIBUTE = "metis.statement"

METIS_QUERY_SPAN_NAME = "metis-query"


def add_quote_to_value_of_type_string(value):
    if isinstance(value, str):
        new_value = str(value).replace("'", "''")
        return "'{}'".format(new_value)  # pylint: disable=consider-using-f-string
    return value


def fix_sql_query(sql, params):
    """without the fix the query is not working because string is not quoted"""
    fixed_param = {
        key: add_quote_to_value_of_type_string(value) for key, value in params.items()
    }
    return sql % fixed_param


def _normalize_vendor(vendor):
    """Return a canonical name for a type of database."""
    if not vendor:
        return "db"  # should this ever happen?

    if "sqlite" in vendor:
        return "sqlite"

    if "postgres" in vendor or vendor == "psycopg2":
        return "postgresql"

    return vendor


class MetisExporter(SpanExporter):
    def __init__(
        self,
        filename,
    ):
        self.dict = {}
        self.filename = filename

    def export(self, spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
        for span in spans:
            trace_id = span.context.trace_id

            if self.dict.get(trace_id) is None:
                self.dict[trace_id] = []

            self.dict[trace_id].append(span)

            if span.parent is None:
                self.export_to_file(trace_id)

        return SpanExportResult.SUCCESS

    def export_to_file(self, trace_id):
        spans = self.dict[trace_id]
        del self.dict[trace_id]

        parent = next(
            x
            for x in spans
            if x.attributes.get(METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER)
        )

        # for now, we don't track sql queries that not under request span
        if not parent:
            return

        spans.remove(parent)

        metis_spans = list(filter(lambda x: x.name == METIS_QUERY_SPAN_NAME, spans))

        if not metis_spans:
            return

        data = {
            "logs": list(
                map(
                    lambda x: {
                        "_uuid": str(uuid.uuid1()),
                        "query": x.attributes.get(METIS_STATEMENT_SPAN_ATTRIBUTE),
                        "dbEngine": x.attributes.get(SpanAttributes.DB_SYSTEM),
                        "date": datetime.utcnow().isoformat(),
                        "plan": json.loads(x.attributes.get(METIS_PLAN_SPAN_ATTRIBUTE))
                        if x.attributes.get(METIS_PLAN_SPAN_ATTRIBUTE)
                        else None,
                    },
                    metis_spans,
                ),
            ),
            "framework": "Flask",
            "path": parent.attributes.get(SpanAttributes.HTTP_TARGET, "N/A"),
            "operationType": parent.attributes.get(SpanAttributes.HTTP_METHOD, "N/A"),
            "requestDuration": (parent.end_time - parent.start_time) / 1000000,
            "requestStatus": parent.attributes.get(
                SpanAttributes.HTTP_STATUS_CODE,
                "N/A",
            ),
        }

        with open(self.filename, "a", encoding="utf8") as file:
            file.write(json.dumps(data) + "\n")


def collect_logs(
    app,
    engine,
    file_name=FILE_NAME,
    plan_collection_option=PlanCollectType.ESTIMATED,
):
    filename = os.getenv("METIS_LOG_FILE_NAME", file_name)

    metis = MetisInstrumentor(filename, plan_collection_option)
    metis.instrument_app(app, engine)


# pylint: disable=too-few-public-methods
class MetisInstrumentor:
    def __init__(self, filename, plan_collection_option):
        self.tracer_provider = TracerProvider()
        self.processor = SimpleSpanProcessor(MetisExporter(filename))
        self.tracer_provider.add_span_processor(self.processor)
        self.tracer = trace.get_tracer(
            "metis",
            "",
            tracer_provider=self.tracer_provider,
        )
        self.plan_collection_option = plan_collection_option

    def instrument_app(self, app, engine):
        def request_hook(
            span,
            flask_request_environ,
        ):  # pylint: disable=unused-argument
            span.set_attribute(METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER, True)

        def response_hook(
            span,
            status,
            response_headers,
        ):  # pylint: disable=unused-argument
            pass

        FlaskInstrumentor().instrument_app(
            app,
            tracer_provider=self.tracer_provider,
            request_hook=request_hook,
            response_hook=response_hook,
        )

        RequestsInstrumentor().instrument()

        db_vendor = _normalize_vendor(engine.name)

        def before_query_hook(  # pylint: disable=too-many-arguments, unused-argument
            conn,
            cursor,
            statement,
            parameters,
            context,
            executemany,
        ):
            if statement.startswith(METIS_DO_NOT_TRACK_COMMENT):
                return statement, parameters

            span = self.tracer.start_span(
                METIS_QUERY_SPAN_NAME,
                kind=trace.SpanKind.CLIENT,
            )

            interpolated_statement = fix_sql_query(statement, parameters)

            span.set_attribute(SpanAttributes.DB_SYSTEM, db_vendor)

            span.set_attribute(METIS_STATEMENT_SPAN_ATTRIBUTE, interpolated_statement)

            if self.plan_collection_option == PlanCollectType.ESTIMATED:
                if conn.dialect.name == "postgresql":
                    with conn.connect() as connection:
                        result = connection.execute(
                            METIS_DO_NOT_TRACK_COMMENT
                            + "explain (verbose, costs, summary, format JSON) "
                            + statement,
                            parameters,
                        )
                        res = result.fetchall()
                        if not res:
                            raise Exception("No plan found")
                        span.set_attribute(
                            METIS_PLAN_SPAN_ATTRIBUTE,
                            json.dumps(res[0][0][0]),
                        )
                else:
                    raise Exception("Plan collection is only supported for PostgreSQL")

            context._metis_span = span  # pylint: disable=protected-access
            return statement, parameters

        listen(engine, "before_cursor_execute", before_query_hook, retval=True)

        def after_cursor_execute(  # pylint: disable=too-many-arguments,unused-argument
            conn,
            cursor,
            statement,
            parameters,
            context,
            executemany,
        ):
            span = getattr(context, "_metis_span", None)
            if span is None:
                return

            span.end()

        listen(engine, "after_cursor_execute", after_cursor_execute)

        def handle_error(context):
            span = getattr(context.execution_context, "_metis_span", None)
            if span is None:
                return

            if span.is_recording():
                span.set_status(
                    Status(
                        StatusCode.ERROR,
                        str(context.original_exception),
                    ),
                )
            span.end()

        listen(engine, "handle_error", handle_error)
