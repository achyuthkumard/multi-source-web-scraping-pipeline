from processing.pipeline import (
    clean_and_validate_records
)


def test_clean_and_validate():

    raw_records = [
        {
            "source": "Books to Scrape",
            "source_url": (
                "https://books.toscrape.com/"
            ),
            "name_or_title": (
                "  Example   Book  "
            ),
            "category": " Fiction ",
            "price": "£25.50",
            "rating": "Four",
            "author": None,
            "tags": None,
            "description": (
                " Some description "
            ),
            "availability": (
                " In stock "
            ),
            "scraped_at": (
                "2026-10-06T00:00:00+00:00"
            ),
        }
    ]

    valid_records, rejected_records = (
        clean_and_validate_records(
            raw_records
        )
    )

    assert len(valid_records) == 1
    assert len(rejected_records) == 0

    record = valid_records[0]

    assert record["name_or_title"] == "Example Book"
    assert record["price"] == 25.50
    assert record["rating"] == 4.0
from processing.pipeline import process_records


def test_complete_processing_pipeline():

    raw_records = [
        {
            "source": "Books to Scrape",
            "source_url": (
                "https://books.toscrape.com/book/"
            ),
            "name_or_title": "Example Book",
            "category": " Fiction ",
            "price": "£25.50",
            "rating": "Four",
            "author": None,
            "tags": None,
            "description": "Example",
            "availability": "In stock",
            "scraped_at": (
                "2026-10-06T00:00:00+00:00"
            ),
        },

        # Duplicate
        {
            "source": "Books to Scrape",
            "source_url": (
                "HTTPS://BOOKS.TOSCRAPE.COM/book"
            ),
            "name_or_title": "Example Book",
            "category": "Fiction",
            "price": "£25.50",
            "rating": "Four",
            "author": None,
            "tags": None,
            "description": "Example",
            "availability": "In stock",
            "scraped_at": (
                "2026-10-06T00:00:00+00:00"
            ),
        },
    ]

    result = process_records(
        raw_records
    )

    assert len(result["valid_records"]) == 2
    assert len(result["rejected_records"]) == 0
    assert len(result["unique_records"]) == 1
    assert len(result["duplicate_records"]) == 1