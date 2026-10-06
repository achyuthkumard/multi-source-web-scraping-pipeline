from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_tags,
    clean_url,
)


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Three") == 3.0


def test_clean_tags():
    assert clean_tags(
        [" change ", "thinking", " world "]
    ) == [
        "change",
        "thinking",
        "world",
    ]


def test_clean_url():
    assert clean_url(
        "https://example.com/test"
    ) == "https://example.com/test"


def test_invalid_url():
    assert clean_url("not-a-url") is None