# Multi-Source Web Scraping & Data Consolidation

## 1. Project Overview

This project implements a Python-based web scraping and data-processing pipeline for collecting information from two public scraping practice websites:

- Books to Scrape
- Quotes to Scrape

The pipeline performs:

1. Web scraping
2. Pagination
3. Data cleaning
4. Data standardization
5. Validation
6. Duplicate detection
7. Data consolidation
8. CSV generation
9. Summary report generation
10. Logging and error handling

The final output is one consolidated dataset containing records from both sources.

---

## 2. Data Sources

### Books to Scrape

URL:

https://books.toscrape.com/

The scraper collects book information such as:

- Book title
- Category
- Price
- Rating
- Availability
- Description
- Product URL

The scraper follows the `Next` pagination link until the final page.

### Quotes to Scrape

URL:

https://quotes.toscrape.com/

The scraper collects:

- Quote text
- Author
- Tags
- Source page URL

The scraper follows the `Next` pagination link until the final page.

---

## 3. Technology Used

- Python 3
- Requests
- BeautifulSoup
- Pandas
- lxml
- Pytest

Python standard-library modules used include:

- pathlib
- json
- logging
- datetime
- re
- urllib.parse
- time
- collections

---

## 4. Project Structure

```text
scrapping_ass/
│
├── scrappers/
│   ├── __init__.py
│   ├── books_scraper.py
│   ├── quotes_scraper.py
│   ├── explore_books.py
│   └── explore_quotes.py
│
├── processing/
│   ├── __init__.py
│   ├── models.py
│   ├── cleaning.py
│   ├── validation.py
│   ├── deduplication.py
│   ├── pipeline.py
│   └── logger.py
│
├── tests/
│   ├── test_models.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   ├── test_deduplication.py
│   └── test_pipeline.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── pipeline.log
│
├── main.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
└── pytest.ini
```

---

## 5. Installation

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

## 6. Requirements

The required Python packages are:

```text
requests
beautifulsoup4
pandas
lxml
pytest
```

---

## 7. How to Run

Run the automated tests:

```powershell
python -m pytest
```

Run the complete scraping pipeline:

```powershell
python main.py
```

The pipeline creates:

```text
output/final_dataset.csv
output/summary_report.json
```

Logs are written to:

```text
logs/pipeline.log
```

---

## 8. Scraping Approach

### Books Scraper

`BooksScraper` uses:

- Requests for HTTP requests
- BeautifulSoup for HTML parsing
- CSS selectors for extracting book information
- The site's `Next` link for pagination

The scraper first extracts records from listing pages.

For each book, its product-detail page is also requested to obtain additional information such as category and description.

### Quotes Scraper

`QuotesScraper` uses:

- Requests for HTTP requests
- BeautifulSoup for HTML parsing
- CSS selectors for quote, author, and tag extraction
- The site's `Next` link for pagination

Both scrapers use source-specific parsing logic so changes in one website do not directly affect the other scraper.

---

## 9. Standardized Data Model

The consolidated dataset uses the following fields:

```text
source
source_url
name_or_title
category
price
rating
author
tags
description
availability
scraped_at
```

Not every source provides every field.

When a field does not apply to a source, the value is kept empty/NULL instead of inventing information.

---

## 10. Data Cleaning

The cleaning layer performs:

### Text cleaning

- Removes leading and trailing whitespace
- Converts repeated whitespace into a single space
- Normalizes empty strings to `None`

Example:

```text
"  Albert    Einstein  "
```

becomes:

```text
"Albert Einstein"
```

### Price cleaning

A Books value such as:

```text
£51.77
```

is converted to:

```text
51.77
```

### Rating cleaning

Books rating words are converted to numeric values:

```text
One   -> 1.0
Two   -> 2.0
Three -> 3.0
Four  -> 4.0
Five  -> 5.0
```

### URL cleaning

URLs are checked to ensure they contain a valid HTTP or HTTPS scheme and network location.

### Tag cleaning

Quote tags are individually cleaned while preserving their list structure.

---

## 11. Validation

Each cleaned record is validated before entering the final dataset.

Validation checks include:

- Recognized source
- Valid source URL
- Required title/quote value
- Numeric price when present
- Non-negative price
- Numeric rating when present
- Rating within the 1–5 range

Invalid records are rejected and their validation reasons are preserved for reporting.

---

## 12. Duplicate Detection

Duplicate detection is performed after cleaning and validation.

### Books

Books are identified primarily using:

```text
source + normalized product URL
```

### Quotes

Quotes are identified using:

```text
source + normalized quote text + normalized author
```

Text normalization removes unnecessary whitespace and ignores capitalization differences.

For example:

```text
"Example Book"
" Example Book "
"EXAMPLE BOOK"
```

are treated as equivalent for duplicate comparison.

Duplicate records are separated from the final unique dataset so that duplicate counts can be included in the summary report.

---

## 13. Error Handling

The scrapers handle common failures such as:

- Connection errors
- HTTP errors
- Timeouts
- Missing HTML elements
- Unexpected HTML structures
- Individual detail-page failures

A failure on an individual book detail page does not unnecessarily stop the complete Books scraper.

Request retry logic is used for temporary request failures where configured.

---

## 14. Logging

Application logs are written to:

```text
logs/pipeline.log
```

The logging output records important events such as:

- Pages being scraped
- Number of records found
- Request failures
- Retry attempts
- Processing results
- Final record counts

Logs are useful for debugging and verifying pipeline execution.

---

## 15. Output Files

### `final_dataset.csv`

Contains the final cleaned, validated, deduplicated records from both sources.

### `summary_report.json`

Contains metrics such as:

- Records collected per source
- Total records collected
- Records after cleaning/validation
- Rejected records
- Duplicate records detected
- Final unique record count
- Final records by source
- Execution time

---

## 16. Testing

Unit tests are implemented using Pytest.

Tests cover:

- Data model creation
- Text cleaning
- Price conversion
- Rating conversion
- URL validation
- Record validation
- Duplicate-key generation
- Duplicate detection
- End-to-end processing logic

Run all tests with:

```powershell
python -m pytest
```

---

## 17. Assumptions

- The provided websites remain publicly accessible.
- The current HTML structure and selectors remain compatible with the scraper.
- A valid book rating is expected to be between 1 and 5.
- Missing source-specific fields are represented as empty/NULL values.
- Duplicate comparison is based on normalized identifying fields rather than exact raw-string equality.

---

## 18. Known Limitations

- Website HTML changes could require selector updates.
- The scraper depends on network availability.
- Some individual detail-page requests may fail or time out.
- The solution is designed for this assignment rather than as a large-scale production scraping system.
- The scraper currently processes records sequentially rather than using parallel processing.

---

## 19. Ethical and Scraping Considerations

Only the public practice websites specified in the assignment are used.

The solution does not attempt to bypass authentication, CAPTCHAs, access controls, or security mechanisms.

Requests are kept reasonable and failures are handled without aggressive repeated traffic.

---

## 20. AI Usage

AI assistance was used during development for:

- Understanding HTML structures
- Designing the project structure
- Developing scraper logic
- Debugging Python errors
- Designing cleaning and validation functions
- Designing duplicate-detection logic
- Creating tests
- Improving documentation

Detailed information is available in:

```text
AI_USAGE.md
```

---

## 21. Final Execution

The complete pipeline can be executed using:

```powershell
python main.py
```

The expected output locations are:

```text
output/final_dataset.csv
output/summary_report.json
logs/pipeline.log
```
