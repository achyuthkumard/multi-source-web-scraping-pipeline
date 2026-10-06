from dataclasses import dataclass
from typing import Optional


@dataclass
class Record:
    source: str
    source_url: Optional[str]
    name_or_title: Optional[str]
    category: Optional[str]
    price: Optional[float]
    rating: Optional[float]
    author: Optional[str]
    tags: Optional[list[str]]
    description: Optional[str]
    availability: Optional[str]
    scraped_at: str