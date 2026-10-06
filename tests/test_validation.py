from processing.validation import validate_record


def valid_book():
    return {
        "source": "Books to Scrape",
        "source_url": (
            "https://books.toscrape.com/"
        ),
        "name_or_title": "Example Book",
        "category": "Fiction",
        "price": 25.50,
        "rating": 4.0,
        "author": None,
        "tags": None,
        "description": "Example description",
        "availability": "In stock",
        "scraped_at": (
            "2026-10-06T00:00:00+00:00"
        ),
    }


def test_valid_record():
    record = valid_book()

    is_valid, errors = validate_record(record)

    assert is_valid is True
    assert errors == []


def test_missing_title():
    record = valid_book()

    record["name_or_title"] = None

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "Missing name_or_title" in errors


def test_invalid_rating():
    record = valid_book()

    record["rating"] = 8

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "Rating must be between 1 and 5" in errors


def test_invalid_price():
    record = valid_book()

    record["price"] = -10

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "Price cannot be negative" in errors


def test_invalid_url():
    record = valid_book()

    record["source_url"] = "not-a-url"

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "Invalid source URL" in errors