import httpx


def assert_link_header(response: httpx.Response, expected_params: dict) -> None:
    request_url = response.request.url
    links = response.headers["Link"].split(", ")
    assert len(links) == len(expected_params)
    for rel, params in expected_params.items():
        expected_url = request_url.copy_with(params=params)
        assert f'<{expected_url}>; rel="{rel}"' in links
