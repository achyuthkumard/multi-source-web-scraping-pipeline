from processing.models import Record


def test_record_creation():
    record = Record(
        source="Books to Scrape",
        source_url="https://example.com/book",
        name_or_title="Example Book",
        category="Fiction",
        price=10.50,
        rating=4.0,
        author=None,
        tags=None,
        description="Example description",
        availability="In stock",
        scraped_at="2026-10-06T00:00:00+00:00"
    )

    assert record.source == "Books to Scrape"
    assert record.name_or_title == "Example Book"
    assert record.price == 10.50
    assert record.rating == 4.0