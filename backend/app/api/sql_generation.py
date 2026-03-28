import re
from typing import Literal, Optional


def generate_pandas_for_graph(
    x_axis: str,
    y_axis: str,
    chart_type: Literal["line", "bar", "doughnut", "scatter", "heatmap", "sankey", "pie"],
) -> dict:
    if chart_type == "doughnut" or chart_type == "pie":
        return {
            "operation": "groupby_sum",
            "group_by": x_axis,
            "value": y_axis,
            "limit": 10,
        }

    if chart_type == "heatmap":
        return {
            "operation": "pivot",
            "x_axis": x_axis,
            "y_axis": y_axis,
            "value": "count",
        }

    if chart_type == "sankey":
        return {
            "operation": "sankey",
            "source": x_axis,
            "target": y_axis,
            "value": "count",
        }

    return {"operation": "select", "columns": [x_axis, y_axis], "limit": 1000}


def generate_time_series_query(
    date_column: str,
    value_column: str,
    frequency: Literal["daily", "weekly", "monthly", "quarterly", "yearly"] = "monthly",
    aggregation: Literal["sum", "avg", "count", "min", "max"] = "sum",
) -> str:
    date_format_map = {
        "daily": "YYYY-MM-DD",
        "weekly": "YYYY-WW",
        "monthly": "YYYY-MM",
        "quarterly": "YYYY-Q",
        "yearly": "YYYY",
    }

    date_expr = f"strftime('%Y-%m-01', {date_column})"

    if frequency == "quarterly":
        date_expr = f"'Q' || (CAST(strftime('%m', {date_column}) AS INTEGER) + 2) / 3 || '-' || strftime('%Y', {date_column})"
    elif frequency == "yearly":
        date_expr = f"strftime('%Y', {date_column})"

    agg_func = aggregation.upper()

    return f"""
SELECT 
    {date_expr} as period,
    {agg_func}({value_column}) as value
FROM data
GROUP BY period
ORDER BY period
"""


def parse_nl_to_pandas(nl_query: str, columns: list[str]) -> dict:
    nl_lower = nl_query.lower()

    if "heatmap" in nl_lower:
        return {"operation": "pivot", "value": "count"}

    if "sankey" in nl_lower:
        return {"operation": "sankey", "value": "count"}

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


def detect_time_series_keywords(query: str) -> Optional[dict]:
    query_lower = query.lower()

    keywords = {
        "daily": ["일별", "하루", "day", "일별"],
        "weekly": ["주별", "一周", "week", "주간"],
        "monthly": ["월별", "달별", "month", "월간"],
        "quarterly": ["분기별", "quarter"],
        "yearly": ["연별", "연간", "year", " 연간"],
    }

    for freq, kws in keywords.items():
        if any(kw in query_lower for kw in kws):
            return {"frequency": freq}

    return None


def parse_heatmap_request(query: str, columns: list[str]) -> dict:
    query_lower = query.lower()

    x_col = None
    y_col = None
    value_col = "count"

    category_cols = [c for c in columns if c.get("data_type") == "category"]
    date_cols = [c for c in columns if c.get("data_type") == "date"]
    number_cols = [c for c in columns if c.get("data_type") == "number"]

    if date_cols and category_cols:
        x_col = date_cols[0]["name"]
        y_col = category_cols[0]["name"]
    elif len(category_cols) >= 2:
        x_col = category_cols[0]["name"]
        y_col = category_cols[1]["name"]
    elif category_cols and number_cols:
        y_col = category_cols[0]["name"]
        x_col = number_cols[0]["name"]
        value_col = "sum"

    return {
        "operation": "pivot",
        "x_axis": x_col,
        "y_axis": y_col,
        "value": value_col,
    }


def parse_sankey_request(query: str, columns: list[str]) -> dict:
    category_cols = [c["name"] for c in columns if c.get("data_type") == "category"]

    if len(category_cols) >= 2:
        return {
            "operation": "sankey",
            "source": category_cols[0],
            "target": category_cols[1],
            "value": "count",
        }

    return {
        "operation": "sankey",
        "source": columns[0]["name"] if columns else "",
        "target": columns[1]["name"] if len(columns) > 1 else "",
        "value": "count",
    }
