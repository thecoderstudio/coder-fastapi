from coderfastapi.lib.requests import RequestWithSession


def test_request_with_session_from_request(mocker):
    request_mock = mocker.MagicMock()
    request_mock.scope = {"type": "http"}
    request_with_session = RequestWithSession.from_request(request_mock)
    assert isinstance(request_with_session, RequestWithSession)
    assert request_with_session.scope == request_mock.scope
    assert request_with_session.receive == request_mock.receive
    assert request_with_session._send == request_mock._send
