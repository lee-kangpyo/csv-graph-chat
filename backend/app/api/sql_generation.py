import re
from typing import Literal


def generate_sql_for_graph(
    table_name: str,
    x_axis: str,
    y_axis: str,
    chart_type: Literal["line", "bar", "doughnut", "scatter"],
) -> str:
    if chart_type == "doughnut":
        return f"SELECT {x_axis}, SUM({y_axis}) as value FROM {table_name} GROUP BY {x_axis} ORDER BY value DESC LIMIT 10"

    if chart_type == "scatter":
        return f"SELECT {x_axis}, {y_axis} FROM {table_name} LIMIT 1000"

    return f"SELECT {x_axis}, {y_axis} FROM {table_name} LIMIT 1000"


def generate_aggregation_sql(
    table_name: str, group_by: str, aggregations: list[dict], limit: int = 100
) -> str:
    agg_parts = []
    for agg in aggregations:
        col = agg.get("column", "")
        func = agg.get("function", "SUM").upper()
        alias = agg.get("alias", f"{func}_{col}")
        agg_parts.append(f"{func}({col}) AS {alias}")

    agg_clause = ", ".join(agg_parts)
    return f"SELECT {group_by}, {agg_clause} FROM {table_name} GROUP BY {group_by} ORDER BY {agg_parts[0].split(' AS ')[1]} DESC LIMIT {limit}"


def parse_nl_to_sql(nl_query: str, table_name: str, columns: list[str]) -> str:
    nl_lower = nl_query.lower()

    if "sum of" in nl_lower or "total" in nl_lower:
        col_match = re.search(r"(sum|total) of (\w+)", nl_lower)
        if col_match:
            col = col_match.group(2)
            return f"SELECT SUM({col}) as total FROM {table_name}"

    if "average" in nl_lower or "avg" in nl_lower:
        col_match = re.search(r"average of (\w+)", nl_lower)
        if col_match:
            col = col_match.group(1)
            return f"SELECT AVG({col}) as average FROM {table_name}"

    if "count" in nl_lower:
        if "group by" in nl_lower:
            col_match = re.search(r"count (\w+) group by (\w+)", nl_lower)
            if col_match:
                count_col = col_match.group(1)
                group_col = col_match.group(2)
                return f"SELECT {group_col}, COUNT({count_col}) as count FROM {table_name} GROUP BY {group_col} LIMIT 50"
        return f"SELECT COUNT(*) as count FROM {table_name}"

    if "top 10" in nl_lower:
        col_match = re.search(r"top 10 by (\w+)", nl_lower)
        if col_match:
            col = col_match.group(1)
            return f"SELECT * FROM {table_name} ORDER BY {col} DESC LIMIT 10"
        return f"SELECT * FROM {table_name} LIMIT 10"

    return f"SELECT * FROM {table_name} LIMIT 100"
