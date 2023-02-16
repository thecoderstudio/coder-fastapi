from coderfastapi.lib.requests import AugmentableRequest


def test_augmentable_request_from_request(mocker):
    request_mock = mocker.MagicMock()
    request_mock.scope = {"type": "http"}
    request_with_session = AugmentableRequest.from_request(request_mock)
    assert isinstance(request_with_session, AugmentableRequest)
    assert request_with_session.scope == request_mock.scope
    assert request_with_session.receive == request_mock.receive
    assert request_with_session._send == request_mock._send
