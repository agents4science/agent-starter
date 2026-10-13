"""Course tracing: one named, replayable trace per work session.

Usage:
    from course_kit import trace

    with trace.session("my-first-agent") as t:
        reply = gateway.chat(messages, headers=t.headers)   # or any client,
        ...                                                  # passing t.headers

Everything called with ``t.headers`` inside the block appears as ONE named
trace in the course viewer (and in your replays), instead of scattered
anonymous requests. At the end, call ``t.finish(task=..., result=...)`` to
record what the session was about (optional but recommended).
"""

import os

from opentelemetry import trace as _otel
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

_PHOENIX = os.environ.get("AGENTS_TRACE_URL", "http://localhost:6006/v1/traces")
_STUDENT = os.environ.get("AGENTS_STUDENT", os.environ.get("USER", "unknown"))

_provider = TracerProvider(resource=Resource.create({"service.name": "cmsc35370"}))
_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint=_PHOENIX)))
_tracer = _provider.get_tracer("course_kit")


class Session:
    def __init__(self, name: str):
        self._span = _tracer.start_span(name)
        ctx = self._span.get_span_context()
        self.name = name
        #: pass these headers on every model call made in this session
        self.headers = {"traceparent": f"00-{ctx.trace_id:032x}-{ctx.span_id:016x}-01"}
        #: include this in the request body so the gateway tags your calls
        self.metadata = {"session_id": name, "student": _STUDENT}
        self._finished = False

    def finish(self, task: str = "", result: str = "") -> None:
        self._span.set_attribute("openinference.span.kind", "AGENT")
        self._span.set_attribute("session.id", self.name)
        self._span.set_attribute("user.id", _STUDENT)
        if task:
            self._span.set_attribute("input.value", task)
        if result:
            self._span.set_attribute("output.value", result)
        self._span.end()
        self._finished = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if not self._finished:
            self.finish()


def session(name: str) -> Session:
    return Session(name)
