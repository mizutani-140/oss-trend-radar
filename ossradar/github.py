"""GitHub Search API client for trending OSS."""

from __future__ import annotations

import httpx

from .models import Repo

SEARCH_URL = "https://api.github.com/search/repositories"
DEFAULT_QUERY = "stars:>10000"


def parse_search_response(data: dict) -> list[Repo]:
    """Map a GitHub Search API response body to a list of Repo."""
    repos: list[Repo] = []
    for item in data.get("items", []):
        repos.append(
            Repo(
                full_name=item["full_name"],
                stars=item.get("stargazers_count", 0),
                language=item.get("language"),
                description=item.get("description"),
                url=item.get("html_url", f"https://github.com/{item['full_name']}"),
            )
        )
    return repos


def fetch_trending(
    query: str = DEFAULT_QUERY,
    *,
    top: int = 10,
    client: httpx.Client | None = None,
    token: str | None = None,
) -> list[Repo]:
    """Fetch the top trending repositories via the GitHub Search API.

    A single Search API call ordered by stars. Pass ``client`` to inject a
    transport (used in tests); otherwise a default client is created.
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": top,
    }

    owns_client = client is None
    if client is None:
        client = httpx.Client(timeout=30.0)
    try:
        response = client.get(SEARCH_URL, params=params, headers=headers)
        response.raise_for_status()
        repos = parse_search_response(response.json())
    finally:
        if owns_client:
            client.close()

    return repos[:top]
