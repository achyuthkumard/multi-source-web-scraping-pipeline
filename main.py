import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from processing.logger import setup_logger

import pandas as pd

from scrappers.books_scraper import BooksScraper
from scrappers.quotes_scraper import QuotesScraper
from processing.pipeline import process_records


# --------------------------------------------------
# Configuration
# --------------------------------------------------

OUTPUT_DIR = Path("output")

FINAL_DATASET_PATH = (
    OUTPUT_DIR / "final_dataset.csv"
)

SUMMARY_PATH = (
    OUTPUT_DIR / "summary_report.json"
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def add_missing_timestamps(records):
    """
    Add scraped_at if a scraper did not provide it.
    Existing timestamps are preserved.
    """

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    for record in records:

        if not record.get("scraped_at"):
            record["scraped_at"] = timestamp

    return records


def count_by_source(records):
    """
    Count records for each source.
    """

    counter = Counter()

    for record in records:

        source = record.get(
            "source",
            "Unknown"
        )

        counter[source] += 1

    return dict(counter)


def prepare_for_csv(records):
    """
    Convert records into a DataFrame-friendly format.

    Lists such as tags are converted into a
    semicolon-separated string.
    """

    rows = []

    for record in records:

        row = dict(record)

        tags = row.get("tags")

        if isinstance(tags, list):
            row["tags"] = "; ".join(tags)

        elif tags is None:
            row["tags"] = ""

        rows.append(row)

    return rows


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():
    logger = setup_logger()

    start_time = time.perf_counter()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 60)
    print("MULTI-SOURCE WEB SCRAPING PIPELINE")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1: Scrape Books
    # --------------------------------------------------

    print("\n[1/4] Scraping Books to Scrape...")

    books_scraper = BooksScraper()

    books = books_scraper.scrape()

    books = add_missing_timestamps(books)

    print(
        f"Books collected: {len(books)}"
    )

    # --------------------------------------------------
    # STEP 2: Scrape Quotes
    # --------------------------------------------------

    print("\n[2/4] Scraping Quotes to Scrape...")

    quotes_scraper = QuotesScraper()

    quotes = quotes_scraper.scrape()

    quotes = add_missing_timestamps(quotes)

    print(
        f"Quotes collected: {len(quotes)}"
    )

    # --------------------------------------------------
    # STEP 3: Combine raw records
    # --------------------------------------------------

    raw_records = books + quotes

    print(
        f"\nTotal records collected: "
        f"{len(raw_records)}"
    )

    # --------------------------------------------------
    # STEP 4: Clean, validate, deduplicate
    # --------------------------------------------------

    print(
        "\n[3/4] Cleaning, validating "
        "and deduplicating..."
    )

    result = process_records(
        raw_records
    )

    valid_records = result[
        "valid_records"
    ]

    rejected_records = result[
        "rejected_records"
    ]

    unique_records = result[
        "unique_records"
    ]

    duplicate_records = result[
        "duplicate_records"
    ]

    print(
        f"Records after cleaning/validation: "
        f"{len(valid_records)}"
    )

    print(
        f"Rejected records: "
        f"{len(rejected_records)}"
    )

    print(
        f"Duplicates detected: "
        f"{len(duplicate_records)}"
    )

    print(
        f"Final unique records: "
        f"{len(unique_records)}"
    )

    # --------------------------------------------------
    # STEP 5: Save final CSV
    # --------------------------------------------------

    print(
        "\n[4/4] Generating output files..."
    )

    csv_rows = prepare_for_csv(
        unique_records
    )

    dataframe = pd.DataFrame(
        csv_rows
    )

    # Keep a predictable column order
    columns = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "availability",
        "scraped_at",
    ]

    dataframe = dataframe.reindex(
        columns=columns
    )

    dataframe.to_csv(
        FINAL_DATASET_PATH,
        index=False,
        encoding="utf-8"
    )

    # --------------------------------------------------
    # STEP 6: Generate summary
    # --------------------------------------------------

    execution_time = (
        time.perf_counter() - start_time
    )

    summary = {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "execution_time_seconds": round(
            execution_time,
            2
        ),

        "records_collected": {
            "Books to Scrape": len(books),
            "Quotes to Scrape": len(quotes),
        },

        "total_records_collected": len(
            raw_records
        ),

        "records_after_cleaning": len(
            valid_records
        ),

        "records_rejected": len(
            rejected_records
        ),

        "duplicates_detected": len(
            duplicate_records
        ),

        "final_record_count": len(
            unique_records
        ),

        "final_records_by_source": (
            count_by_source(
                unique_records
            )
        ),

        "rejected_records_by_source": (
            count_by_source(
                [
                    item["record"]
                    for item in rejected_records
                ]
            )
        ),

        "duplicate_records_by_source": (
            count_by_source(
                [
                    item["record"]
                    for item in duplicate_records
                ]
            )
        ),
    }

    with open(
        SUMMARY_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # Final output
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED")
    print("=" * 60)

    print(
        f"CSV:     {FINAL_DATASET_PATH}"
    )

    print(
        f"Summary: {SUMMARY_PATH}"
    )

    print(
        f"Time:    {execution_time:.2f} seconds"
    )


if __name__ == "__main__":
    main()