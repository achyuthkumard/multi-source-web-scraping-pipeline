# AI Usage

## 1. AI Tool Used

Tool:

ChatGPT

AI assistance was used during development of the Python web scraping and data-processing assignment.

---

## 2. Areas Where AI Was Used

AI assistance was used for:

- Understanding the HTML structure of Books to Scrape
- Understanding the HTML structure of Quotes to Scrape
- Designing the project folder structure
- Developing initial scraper logic
- Understanding pagination
- Debugging Python and pytest errors
- Designing cleaning functions
- Designing validation rules
- Designing duplicate-detection logic
- Designing unit tests
- Improving error handling and logging
- Preparing project documentation

---

## 3. Representative Prompts

Examples of prompts used during development:

### Scraper design

"Help me build a Python web scraper for Books to Scrape using Requests and BeautifulSoup with pagination."

### HTML understanding

"Explain how to identify the book title, price, rating, availability and product URL from the Books to Scrape HTML."

### Data processing

"Help me design reusable cleaning functions for text normalization, price conversion, rating conversion and URL validation."

### Deduplication

"How can I detect duplicate records when capitalization, whitespace and URL formatting may differ?"

### Testing

"Help me create Pytest unit tests for the cleaning, validation and deduplication functions."

### Debugging

"Why am I getting ModuleNotFoundError when running pytest, and how should I fix the project structure?"

### Error handling

"How should I add retries, logging, timeouts and graceful handling of individual page failures to this scraper?"

---

## 4. AI-Assisted Code Areas

AI assistance contributed to initial ideas and code drafts for:

- `books_scraper.py`
- `quotes_scraper.py`
- `processing/cleaning.py`
- `processing/validation.py`
- `processing/deduplication.py`
- `processing/pipeline.py`
- test files
- logging approach
- `README.md`

The code was reviewed and adapted during implementation.

---

## 5. Changes Made After Reviewing AI Output

Several changes were made during development instead of blindly using the generated code.

Examples:

1. The project initially had an import problem when pytest could not locate the `processing` package. The project structure was checked and `__init__.py` was added/verified.

2. A data-model mismatch was discovered where the scrapers were returning `Record` objects while the processing layer expected dictionaries. The scraper outputs were changed back to dictionaries so the architecture consistently follows:

   Scraping → Raw dictionaries → Cleaning → Validation → Deduplication.

3. Temporary one-page limits were used during development to avoid repeatedly scraping all pages while debugging.

4. The scraper was tested against actual pagination rather than assuming a fixed number of pages.

---

## 6. AI Suggestions That Required Correction

One important implementation issue was a mismatch between the `Record` dataclass and the dictionary-based processing functions.

The error was:

```text
AttributeError: 'Record' object has no attribute 'get'
```

The issue was identified during execution and corrected by making the scrapers return dictionaries consistently.

This demonstrates that AI-generated code was reviewed and tested rather than submitted without verification.

---

## 7. Verification and Testing

The solution was tested incrementally.

Tests were created for:

- Data model creation
- Cleaning functions
- Validation
- Duplicate detection
- Processing pipeline

Pytest was used to execute the tests:

```powershell
python -m pytest
```

The scraper was also executed through:

```powershell
python main.py
```

The generated output was checked for:

```text
output/final_dataset.csv
output/summary_report.json
logs/pipeline.log
```

Scraping was observed to continue through the Books pagination pages even when an individual book-detail request timed out, demonstrating graceful handling of an individual request failure.

---

## 8. Candidate Responsibility

AI was used as a development aid, but the final implementation was reviewed, executed, debugged, tested, and adapted manually.

The candidate is responsible for understanding the final implementation and being able to explain:

- Scraper architecture
- Pagination
- HTML selectors
- Data cleaning
- Validation
- Duplicate detection
- Error handling
- Logging
- Output generation
- Testing
