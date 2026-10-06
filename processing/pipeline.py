from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import deduplicate_records


def clean_and_validate_records(raw_records):

    valid_records = []
    rejected_records = []

    for raw_record in raw_records:

        cleaned_record = clean_record(
            raw_record
        )

        is_valid, errors = validate_record(
            cleaned_record
        )

        if is_valid:

            valid_records.append(
                cleaned_record
            )

        else:

            rejected_records.append({
                "record": cleaned_record,
                "errors": errors,
            })

    return valid_records, rejected_records


def process_records(raw_records):

    # Step 1 + Step 2:
    # Clean and validate
    valid_records, rejected_records = (
        clean_and_validate_records(
            raw_records
        )
    )

    # Step 3:
    # Deduplicate
    unique_records, duplicate_records = (
        deduplicate_records(
            valid_records
        )
    )

    return {
        "valid_records": valid_records,
        "rejected_records": rejected_records,
        "unique_records": unique_records,
        "duplicate_records": duplicate_records,
    }