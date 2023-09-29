from unittest.mock import patch

from coderfastapi.logging.middleware import TRACE_HEADER, LoggingMiddleware


async def test_logging_middleware_call(mocker):
    trace_header_val = "TRACE HEADER"
    scope = {"type": "http"}
    app_mock = mocker.AsyncMock()
    receive_mock = mocker.MagicMock()
    send_mock = mocker.MagicMock()
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    request_mock = mocker.MagicMock(headers={TRACE_HEADER: trace_header_val})
    logging_middleware = LoggingMiddleware(
        app=app_mock,
        cloud_trace_context=trace_context_mock,
        http_request_context=request_context_mock,
    )

    with (
        patch(
            "coderfastapi.logging.middleware.HTTPRequestSchema.from_request"
        ) as schema_from_request_mock,
        patch(
            "coderfastapi.logging.middleware.Request", return_value=request_mock
        ) as request_init_mock,
    ):
        await logging_middleware.__call__(scope, receive_mock, send_mock)

    trace_context_mock.set.assert_called_once_with(trace_header_val)
    schema_from_request_mock.assert_called_once_with(request_mock)
    request_context_mock.set.assert_called_once_with(
        schema_from_request_mock(request_mock)
    )
    request_init_mock.assert_called_once_with(scope, receive=receive_mock)
    app_mock.assert_awaited_once_with(scope, receive_mock, send_mock)


async def test_logging_middleware_call_without_cloud_trace(mocker):
    scope = {"type": "http"}
    app_mock = mocker.AsyncMock()
    receive_mock = mocker.MagicMock()
    send_mock = mocker.MagicMock()
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    request_mock = mocker.MagicMock(headers={})
    logging_middleware = LoggingMiddleware(
        app=app_mock,
        cloud_trace_context=trace_context_mock,
        http_request_context=request_context_mock,
    )

    with (
        patch(
            "coderfastapi.logging.middleware.HTTPRequestSchema.from_request"
        ) as schema_from_request_mock,
        patch(
            "coderfastapi.logging.middleware.Request", return_value=request_mock
        ) as request_init_mock,
    ):
        await logging_middleware.__call__(scope, receive_mock, send_mock)

    trace_context_mock.set.assert_not_called()
    schema_from_request_mock.assert_called_once_with(request_mock)
    request_context_mock.set.assert_called_once_with(
        schema_from_request_mock(request_mock)
    )
    request_init_mock.assert_called_once_with(scope, receive=receive_mock)
    app_mock.assert_awaited_once_with(scope, receive_mock, send_mock)


async def test_logging_middleware_call_not_http_request(mocker):
    scope = {"type": "websocket"}
    app_mock = mocker.AsyncMock()
    receive_mock = mocker.MagicMock()
    send_mock = mocker.MagicMock()
    trace_context_mock = mocker.MagicMock()
    request_context_mock = mocker.MagicMock()
    logging_middleware = LoggingMiddleware(
        app=app_mock,
        cloud_trace_context=trace_context_mock,
        http_request_context=request_context_mock,
    )

    await logging_middleware.__call__(scope, receive_mock, send_mock)

    trace_context_mock.set.assert_not_called()
    request_context_mock.set.assert_not_called()
    app_mock.assert_awaited_once_with(scope, receive_mock, send_mock)
