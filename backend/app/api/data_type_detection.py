import re
from typing import Literal, Any
from datetime import datetime

DataType = Literal["date", "number", "category", "boolean", "unknown"]

DATE_PATTERNS = [
    r"^\d{4}-\d{2}-\d{2}$",
    r"^\d{4}/\d{2}/\d{2}$",
    r"^\d{2}-\d{2}-\d{4}$",
    r"^\d{2}/\d{2}/\d{4}$",
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}",
    r"^[A-Za-z]{3}\s+\d{1,2},?\s+\d{4}$",
]

BOOLEAN_VALUES = {"true", "false", "yes", "no", "1", "0", "t", "f", "y", "n"}


def try_parse_date(value: str) -> bool:
    for pattern in DATE_PATTERNS:
        if re.match(pattern, str(value).strip()):
            return True
    try:
        datetime.fromisoformat(str(value).strip().replace("/", "-"))
        return True
    except:
        pass
    return False


def detect_data_type(values: list[str], sample_size: int = 100) -> DataType:
    if not values:
        return "unknown"

    sample = [
        str(v).strip()
        for v in values[:sample_size]
        if v is not None and str(v).strip() != ""
    ]

    if not sample:
        return "unknown"

    date_count = 0
    number_count = 0
    boolean_count = 0
    category_count = 0

    for value in sample:
        lower_val = value.lower()

        if lower_val in BOOLEAN_VALUES:
            boolean_count += 1
        elif try_parse_date(value):
            date_count += 1
        elif re.match(r"^-?\d+\.?\d*$", value):
            number_count += 1
        else:
            category_count += 1

    total = len(sample)
    threshold = 0.8

    if boolean_count / total >= threshold:
        return "boolean"
    if date_count / total >= threshold:
        return "date"
    if number_count / total >= threshold:
        return "number"

    return "category"


def detect_column_types(headers: list[str], rows: list[list[Any]]) -> dict:
    column_types = {}

    for i, header in enumerate(headers):
        values = [row[i] if i < len(row) else None for row in rows]
        detected_type = detect_data_type(values)
        sample_values = [str(v) for v in values[:5] if v is not None]
        column_types[header] = {"type": detected_type, "sample_values": sample_values}

    return column_types
