import re
from urllib.parse import urlparse


RATING_MAP = {
    "One": 1.0,
    "Two": 2.0,
    "Three": 3.0,
    "Four": 4.0,
    "Five": 5.0,
}


def clean_text(value):
    """
    Remove unnecessary whitespace and normalize text.
    """
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Replace multiple whitespace characters with one space
    value = re.sub(r"\s+", " ", value)

    return value


def clean_price(value):
    """
    Convert a price such as '£51.77' into 51.77.
    """
    if value is None:
        return None

    value = str(value).strip()

    # Keep digits and decimal point
    value = re.sub(r"[^\d.]", "", value)

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_rating(value):
    """
    Convert Books to Scrape ratings such as 'Three'
    into numeric values.
    """
    if value is None:
        return None

    value = str(value).strip()

    if value in RATING_MAP:
        return RATING_MAP[value]

    # Also support an already numeric rating
    try:
        rating = float(value)

        if 1.0 <= rating <= 5.0:
            return rating

    except ValueError:
        pass

    return None


def clean_tags(tags):
    """
    Clean quote tags while preserving the list structure.
    """
    if not tags:
        return None

    cleaned_tags = []

    for tag in tags:
        cleaned = clean_text(tag)

        if cleaned:
            cleaned_tags.append(cleaned)

    return cleaned_tags if cleaned_tags else None


def clean_url(url):
    """
    Validate that a URL is HTTP/HTTPS and has a network location.
    """
    if not url:
        return None

    url = str(url).strip()

    try:
        parsed = urlparse(url)

        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return url

    except ValueError:
        pass

    return None


def clean_record(record):
    """
    Clean one raw scraped record.
    """
    return {
        "source": clean_text(record.get("source")),
        "source_url": clean_url(record.get("source_url")),
        "name_or_title": clean_text(
            record.get("name_or_title")
        ),
        "category": clean_text(
            record.get("category")
        ),
        "price": clean_price(
            record.get("price")
        ),
        "rating": clean_rating(
            record.get("rating")
        ),
        "author": clean_text(
            record.get("author")
        ),
        "tags": clean_tags(
            record.get("tags")
        ),
        "description": clean_text(
            record.get("description")
        ),
        "availability": clean_text(
            record.get("availability")
        ),
        "scraped_at": clean_text(
            record.get("scraped_at")
        ),
    }