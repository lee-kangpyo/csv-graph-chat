def generate_insight_prompt(
    columns: list[dict], row_count: int, user_question: str = None
) -> str:
    column_info = []
    for col in columns:
        col_info = f"- {col['name']}: {col['data_type']}"
        if col.get("inferred_name"):
            col_info += f" (meaning: {col['inferred_name']})"
        if col.get("sample_values"):
            samples = ", ".join([str(v) for v in col["sample_values"][:3]])
            col_info += f" [e.g., {samples}]"
        column_info.append(col_info)

    base_prompt = f"""You are a data analyst AI. A user has uploaded a CSV file with {row_count} rows and the following columns:

{chr(10).join(column_info)}

The user wants to understand their data and generate insights."""

    if user_question:
        base_prompt += f"""

The user specifically asked: "{user_question}"
"""
    else:
        base_prompt += """

Ask the user what kind of insights they want, or suggest 2-3 potential analyses based on the data types detected.
"""

    base_prompt += """

Provide a helpful, conversational response that guides the user toward actionable insights."""

    return base_prompt


def generate_graph_suggestion_prompt(columns: list[dict], user_request: str) -> str:
    column_names = [col["name"] for col in columns]
    column_types = {col["name"]: col["data_type"] for col in columns}

    prompt = f"""The user wants to create a graph with this request: "{user_request}"

Available columns: {", ".join(column_names)}
Column types: {column_types}

Based on the user's request and the available data, suggest:
1. The best chart type (line, bar, doughnut, or scatter)
2. Which column should be on the X axis
3. Which column should be on the Y axis
4. A descriptive title for the chart

Respond in JSON format:
{{
  "chart_type": "bar",
  "x_axis": "region",
  "y_axis": "sales",
  "title": "Sales by Region"
}}
"""
    return prompt


def parse_graph_suggestion(response_content: str, columns: list[dict] = None) -> dict:
    import json

    column_names = [col["name"] for col in columns] if columns else []

    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        return {
            "chart_type": "bar",
            "x_axis": column_names[0] if column_names else "",
            "y_axis": column_names[1] if len(column_names) > 1 else "",
            "title": "Chart",
        }
