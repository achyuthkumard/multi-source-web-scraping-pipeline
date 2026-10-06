from urllib.parse import urlparse


VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape",
}


def is_valid_url(url):
    if not url:
        return False

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    except ValueError:
        return False


def validate_record(record):
    """
    Validate one cleaned record.

    Returns:
        (True, [])
        or
        (False, [reason1, reason2, ...])
    """

    errors = []

    # -------------------------
    # Source validation
    # -------------------------

    source = record.get("source")

    if source not in VALID_SOURCES:
        errors.append("Invalid source")

    # -------------------------
    # URL validation
    # -------------------------

    source_url = record.get("source_url")

    if not is_valid_url(source_url):
        errors.append("Invalid source URL")

    # -------------------------
    # Name/title validation
    # -------------------------

    name_or_title = record.get("name_or_title")

    if not name_or_title:
        errors.append("Missing name_or_title")

    # -------------------------
    # Price validation
    # -------------------------

    price = record.get("price")

    if price is not None:

        if not isinstance(price, (int, float)):
            errors.append("Price is not numeric")

        elif price < 0:
            errors.append("Price cannot be negative")

    # -------------------------
    # Rating validation
    # -------------------------

    rating = record.get("rating")

    if rating is not None:

        if not isinstance(rating, (int, float)):
            errors.append("Rating is not numeric")

        elif not 1 <= rating <= 5:
            errors.append(
                "Rating must be between 1 and 5"
            )

    # -------------------------
    # Final result
    # -------------------------

    return len(errors) == 0, errors