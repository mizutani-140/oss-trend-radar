from dataclasses import dataclass


@dataclass(frozen=True)
class Repo:
    """A single GitHub repository entry in a trend report."""

    full_name: str
    stars: int
    language: str | None
    description: str | None
    url: str
