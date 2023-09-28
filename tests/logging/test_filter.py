from unittest.mock import patch

from coderfastapi.logging.filter import CloudLoggingFilter


def test_cloud_logging_filter_minimal(mocker):
    project = "GCP project"
    record = mocker.MagicMock(trace=None, span_id=None, http_request=None)
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    trace_context_mock.get.return_value = (None, None)
    request_context_mock.get.return_value = None

    with patch(
        "coderfastapi.logging.filter.GoogleCloudLoggingFilter.filter",
        return_value=True,
    ):
        assert CloudLoggingFilter(
            trace_context_mock,
            request_context_mock,
            project=project,
        ).filter(record)

    assert record.trace is None
    assert record.span_id is None
    assert record.http_request is None


def test_cloud_logging_filter_complete(mocker):
    project = "GCP project"
    trace_id = "TRACE_ID"
    span_id = "SPAN_ID"
    http_request_schema_mock = mocker.MagicMock()
    record = mocker.MagicMock(trace=None, span_id=None, http_request=None)
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    trace_context_mock.get.return_value = (trace_id, span_id)
    request_context_mock.get.return_value = http_request_schema_mock

    with patch(
        "coderfastapi.logging.filter.GoogleCloudLoggingFilter.filter",
        return_value=True,
    ):
        assert CloudLoggingFilter(
            trace_context_mock,
            request_context_mock,
            project=project,
        ).filter(record)

    assert record.trace == f"projects/{project}/traces/{trace_id}"
    assert record.span_id == span_id
    assert record.http_request == http_request_schema_mock.dict(by_alias=True)
