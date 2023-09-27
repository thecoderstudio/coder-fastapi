from coderfastapi.lib.logging.context import (
    CLOUD_TRACE_CONTEXT_NAME,
    HTTP_REQUEST_CONTEXT_NAME,
    cloud_trace_context,
    http_request_context,
)


def test_cloud_trace_context_name():
    assert cloud_trace_context.name == CLOUD_TRACE_CONTEXT_NAME


def test_cloud_trace_context_default():
    assert cloud_trace_context.get() == (None, None)


def test_cloud_trace_context_set():
    cloud_trace_context.set("TRACE_ID/SPAN_ID;o=TRACE_TRUE")
    trace_id, span_id = cloud_trace_context.get()
    assert trace_id == "TRACE_ID"
    assert span_id == "SPAN_ID"


def test_http_request_context_name():
    assert http_request_context.name == HTTP_REQUEST_CONTEXT_NAME


def test_http_request_context_default():
    assert http_request_context.get() is None
