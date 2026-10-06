import re
from urllib.parse import urlparse, urlunparse


def normalize_text_for_key(value):
    """
    Normalize text for duplicate comparison.

    Example:
        '  Example   Book  '
        'EXAMPLE BOOK'

    Both become:
        'example book'
    """

    if value is None:
        return ""

    value = str(value).strip().lower()

    value = re.sub(r"\s+", " ", value)

    return value


def normalize_url_for_key(url):
    """
    Normalize a URL for duplicate comparison.
    """

    if not url:
        return ""

    try:
        parsed = urlparse(str(url).strip())

        # Remove trailing slash from path
        path = parsed.path.rstrip("/")

        normalized = urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            "",
            parsed.query,
            ""
        ))

        return normalized

    except ValueError:
        return normalize_text_for_key(url)


def get_duplicate_key(record):
    """
    Generate a deterministic duplicate key.

    Books:
        source + source_url

    Quotes:
        source + quote text + author

    Other sources:
        source + title + author + category
    """

    source = normalize_text_for_key(
        record.get("source")
    )

    # Books
    if source == "books to scrape":

        source_url = normalize_url_for_key(
            record.get("source_url")
        )

        if source_url:
            return (
                "books",
                source_url
            )

    # Quotes
    if source == "quotes to scrape":

        quote_text = normalize_text_for_key(
            record.get("name_or_title")
        )

        author = normalize_text_for_key(
            record.get("author")
        )

        return (
            "quotes",
            quote_text,
            author
        )

    # Generic fallback
    return (
        source,
        normalize_text_for_key(
            record.get("name_or_title")
        ),
        normalize_text_for_key(
            record.get("author")
        ),
        normalize_text_for_key(
            record.get("category")
        )
    )


def deduplicate_records(records):
    """
    Remove duplicates while preserving the first occurrence.

    Returns:
        unique_records
        duplicate_records
    """

    seen = set()

    unique_records = []
    duplicate_records = []

    for record in records:

        key = get_duplicate_key(record)

        if key in seen:

            duplicate_records.append({
                "record": record,
                "duplicate_key": key
            })

        else:

            seen.add(key)
            unique_records.append(record)

    return unique_records, duplicate_records