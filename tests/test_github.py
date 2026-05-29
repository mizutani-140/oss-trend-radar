import httpx

from ossradar.github import SEARCH_URL, fetch_trending, parse_search_response
from ossradar.models import Repo

SAMPLE_RESPONSE = {
    "total_count": 2,
    "items": [
        {
            "full_name": "octocat/hello-world",
            "stargazers_count": 12345,
            "language": "Python",
            "description": "A sample trending repository",
            "html_url": "https://github.com/octocat/hello-world",
        },
        {
            "full_name": "acme/widgets",
            "stargazers_count": 987,
            "language": None,
            "description": None,
            "html_url": "https://github.com/acme/widgets",
        },
    ],
}


def test_parse_search_response_maps_fields():
    repos = parse_search_response(SAMPLE_RESPONSE)
    assert repos == [
        Repo(
            full_name="octocat/hello-world",
            stars=12345,
            language="Python",
            description="A sample trending repository",
            url="https://github.com/octocat/hello-world",
        ),
        Repo(
            full_name="acme/widgets",
            stars=987,
            language=None,
            description=None,
            url="https://github.com/acme/widgets",
        ),
    ]


def test_fetch_trending_calls_search_endpoint_and_parses():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["query"] = dict(request.url.params)
        return httpx.Response(200, json=SAMPLE_RESPONSE)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    repos = fetch_trending("stars:>10000", top=2, client=client)

    assert captured["url"].startswith(SEARCH_URL)
    assert captured["query"]["q"] == "stars:>10000"
    assert captured["query"]["per_page"] == "2"
    assert captured["query"]["sort"] == "stars"
    assert [r.full_name for r in repos] == ["octocat/hello-world", "acme/widgets"]


def test_fetch_trending_truncates_to_top_n():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SAMPLE_RESPONSE)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    repos = fetch_trending("stars:>10000", top=1, client=client)
    assert len(repos) == 1
    assert repos[0].full_name == "octocat/hello-world"
