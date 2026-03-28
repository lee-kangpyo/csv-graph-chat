import re
from typing import Literal


def generate_pandas_for_graph(
    x_axis: str,
    y_axis: str,
    chart_type: Literal["line", "bar", "doughnut", "scatter"],
) -> dict:
    if chart_type == "doughnut":
        return {
            "operation": "groupby_sum",
            "group_by": x_axis,
            "value": y_axis,
            "limit": 10,
        }

    return {"operation": "select", "columns": [x_axis, y_axis], "limit": 1000}


def parse_nl_to_pandas(nl_query: str, columns: list[str]) -> dict:
    nl_lower = nl_query.lower()

    if "sum of" in nl_lower or "total" in nl_lower:
        col_match = re.search(r"(sum|total) of (\w+)", nl_lower)
        if col_match:
            col = col_match.group(2)
            return {"operation": "sum", "column": col}

    if "average" in nl_lower or "avg" in nl_lower:
        col_match = re.search(r"average of (\w+)", nl_lower)
        if col_match:
            col = col_match.group(1)
            return {"operation": "mean", "column": col}

    if "count" in nl_lower:
        if "group by" in nl_lower:
            col_match = re.search(r"count (\w+) group by (\w+)", nl_lower)
            if col_match:
                count_col = col_match.group(1)
                group_col = col_match.group(2)
                return {
                    "operation": "count_groupby",
                    "count_col": count_col,
                    "group_col": group_col,
                }
        return {"operation": "count"}

    if "top 10" in nl_lower:
        col_match = re.search(r"top 10 by (\w+)", nl_lower)
        if col_match:
            col = col_match.group(1)
            return {"operation": "top_n", "column": col, "n": 10}
        return {"operation": "head", "n": 10}

    return {"operation": "head", "n": 100}
