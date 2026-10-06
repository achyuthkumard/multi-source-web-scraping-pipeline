import json
from pathlib import Path

import pandas as pd
import streamlit as st

from scrappers.books_scraper import BooksScraper
from scrappers.quotes_scraper import QuotesScraper
from processing.pipeline import process_records


OUTPUT_DIR = Path("output")
CSV_PATH = OUTPUT_DIR / "final_dataset.csv"
SUMMARY_PATH = OUTPUT_DIR / "summary_report.json"


st.set_page_config(
    page_title="Web Scraping Pipeline",
    page_icon="🕷️",
    layout="wide"
)

st.title("🕷️ Multi-Source Web Scraping Pipeline")
st.write(
    "Scraping, cleaning, validation, deduplication and "
    "consolidation of Books to Scrape and Quotes to Scrape."
)


def run_pipeline():
    books_scraper = BooksScraper()
    quotes_scraper = QuotesScraper()

    books = books_scraper.scrape()
    quotes = quotes_scraper.scrape()

    raw_records = books + quotes

    result = process_records(raw_records)

    unique_records = result["unique_records"]

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = []

    for record in unique_records:
        row = dict(record)

        if isinstance(row.get("tags"), list):
            row["tags"] = "; ".join(row["tags"])

        rows.append(row)

    dataframe = pd.DataFrame(rows)

    dataframe.to_csv(
        CSV_PATH,
        index=False,
        encoding="utf-8"
    )

    summary = {
        "books_collected": len(books),
        "quotes_collected": len(quotes),
        "total_collected": len(raw_records),
        "valid_records": len(result["valid_records"]),
        "rejected_records": len(result["rejected_records"]),
        "duplicates_detected": len(
            result["duplicate_records"]
        ),
        "final_records": len(unique_records),
    }

    with open(
        SUMMARY_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            summary,
            file,
            indent=4
        )

    return dataframe, summary


# --------------------------------------------------
# Existing output
# --------------------------------------------------

if CSV_PATH.exists():

    dataframe = pd.read_csv(CSV_PATH)

    st.success(
        "Existing consolidated dataset loaded."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Records",
            len(dataframe)
        )

    with col2:
        st.metric(
            "Books",
            int(
                (dataframe["source"] == "Books to Scrape")
                .sum()
            )
        )

    with col3:
        st.metric(
            "Quotes",
            int(
                (dataframe["source"] == "Quotes to Scrape")
                .sum()
            )
        )

    st.subheader("Dataset Preview")

    st.dataframe(
        dataframe,
        use_container_width=True
    )

    csv_data = dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Final Dataset",
        data=csv_data,
        file_name="final_dataset.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# Run fresh scrape
# --------------------------------------------------

st.subheader("Run Pipeline")

if st.button(
    "🚀 Run Fresh Scraping Pipeline",
    type="primary"
):

    with st.spinner(
        "Scraping and processing data..."
    ):

        try:

            dataframe, summary = run_pipeline()

            st.success(
                "Pipeline completed successfully."
            )

            st.json(summary)

            st.subheader(
                "Fresh Dataset"
            )

            st.dataframe(
                dataframe,
                use_container_width=True
            )

        except Exception as error:

            st.error(
                f"Pipeline failed: {error}"
            )