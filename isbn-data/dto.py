from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BookData:
    title: str
    authors: list[dict[str, str]]
    year: int
    publisher: Optional[str] = ""
    issue_number: Optional[str] = ""
    place: Optional[str] = ""
    pages_number: Optional[int] = None
