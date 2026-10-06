from processing.deduplication import (
    normalize_text_for_key,
    normalize_url_for_key,
    get_duplicate_key,
    deduplicate_records,
)


def test_normalize_text():

    assert normalize_text_for_key(
        "  Example   Book  "
    ) == "example book"


def test_normalize_url():

    assert normalize_url_for_key(
        "HTTPS://EXAMPLE.COM/book/"
    ) == "https://example.com/book"


def test_books_duplicate_key():

    record1 = {
        "source": "Books to Scrape",
        "source_url": (
            "https://books.toscrape.com/book/"
        ),
    }

    record2 = {
        "source": "Books to Scrape",
        "source_url": (
            "HTTPS://BOOKS.TOSCRAPE.COM/book"
        ),
    }

    assert get_duplicate_key(
        record1
    ) == get_duplicate_key(record2)
    
def test_quotes_duplicate_key():

    record1 = {
        "source": "Quotes to Scrape",
        "name_or_title": (
            "The World as We Have Created It"
        ),
        "author": "Albert Einstein",
    }

    record2 = {
        "source": "Quotes to Scrape",
        "name_or_title": (
            "  the world   as we have created it "
        ),
        "author": "ALBERT   EINSTEIN",
    }

    assert get_duplicate_key(
        record1
    ) == get_duplicate_key(record2)


def test_deduplicate_records():

    records = [
        {
            "source": "Books to Scrape",
            "source_url": (
                "https://books.toscrape.com/book/"
            ),
            "name_or_title": "Example Book",
        },
        {
            "source": "Books to Scrape",
            "source_url": (
                "HTTPS://BOOKS.TOSCRAPE.COM/book"
            ),
            "name_or_title": "Example Book",
        },
        {
            "source": "Books to Scrape",
            "source_url": (
                "https://books.toscrape.com/book-2"
            ),
            "name_or_title": "Another Book",
        },
    ]

    unique_records, duplicate_records = (
        deduplicate_records(records)
    )

    assert len(unique_records) == 2
    assert len(duplicate_records) == 1