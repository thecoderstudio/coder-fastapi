from unittest.mock import patch

from coderfastapi.logging.middleware import TRACE_HEADER, LoggingMiddleware


async def test_logging_middleware_dispatch(mocker):
    trace_header_val = "TRACE HEADER"
    app_mock = mocker.MagicMock()
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    request_mock = mocker.MagicMock(headers={TRACE_HEADER: trace_header_val})
    call_next_mock = mocker.AsyncMock()
    logging_middleware = LoggingMiddleware(
        trace_context_mock,
        request_context_mock,
        app=app_mock,
    )

    with patch(
        "coderfastapi.logging.middleware.HTTPRequestSchema.from_request"
    ) as schema_from_request_mock:
        await logging_middleware.dispatch(request_mock, call_next_mock)

    trace_context_mock.set.assert_called_once_with(trace_header_val)
    schema_from_request_mock.assert_called_once_with(request_mock)
    request_context_mock.set.assert_called_once_with(
        schema_from_request_mock(request_mock)
    )

    call_next_mock.assert_awaited_once_with(request_mock)


async def test_logging_middleware_dispatch_without_cloud_trace(mocker):
    app_mock = mocker.MagicMock()
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    request_mock = mocker.MagicMock(headers={})
    call_next_mock = mocker.AsyncMock()
    logging_middleware = LoggingMiddleware(
        trace_context_mock,
        request_context_mock,
        app=app_mock,
    )

    with patch(
        "coderfastapi.logging.middleware.HTTPRequestSchema.from_request"
    ) as schema_from_request_mock:
        await logging_middleware.dispatch(request_mock, call_next_mock)

    trace_context_mock.set.assert_not_called()
    schema_from_request_mock.assert_called_once_with(request_mock)
    request_context_mock.set.assert_called_once_with(
        schema_from_request_mock(request_mock)
    )

    call_next_mock.assert_awaited_once_with(request_mock)
