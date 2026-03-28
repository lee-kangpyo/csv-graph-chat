import re
from typing import Literal

MEANINGLESS_HEADERS = {
    "col",
    "column",
    "field",
    "data",
    "value",
    "var",
    "variable",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "v1",
    "v2",
    "v3",
    "v4",
    "v5",
    "v6",
    "v7",
    "v8",
    "v9",
    "v10",
    "column1",
    "column2",
    "column3",
    "field1",
    "field2",
    "field3",
    "untitled",
    "undefined",
    "null",
    "none",
}


def is_meaningless_header(header: str) -> bool:
    normalized = header.strip().lower()
    if not normalized:
        return True
    if normalized in MEANINGLESS_HEADERS:
        return True
    if re.match(r"^col\d+$", normalized):
        return True
    if re.match(r"^field\d+$", normalized):
        return True
    if re.match(r"^var\d+$", normalized):
        return True
    return False


def detect_header_status(headers: list[str]) -> dict:
    meaningful = []
    meaningless = []
    missing = []

    for header in headers:
        if not header or header.strip() == "":
            missing.append(header)
        elif is_meaningless_header(header):
            meaningless.append(header)
        else:
            meaningful.append(header)

    return {
        "meaningful": meaningful,
        "meaningless": meaningless,
        "missing": missing,
        "all_meaningful": len(meaningful) == len(headers) and len(missing) == 0,
    }
