from typing import Literal

DataType = Literal["date", "number", "category", "boolean", "unknown"]


def generate_column_inference_prompt(columns: list[dict]) -> str:
    column_descriptions = []
    for col in columns:
        desc = f"- {col['name']}: detected as {col['data_type']}"
        if col.get("sample_values"):
            samples = ", ".join([str(v) for v in col["sample_values"][:3]])
            desc += f" (examples: {samples})"
        column_descriptions.append(desc)

    prompt = f"""You are a data analyst helping to interpret CSV column names.

Given the following columns detected in a CSV file:

{chr(10).join(column_descriptions)}

Some columns may have meaningless names (like "col1", "field2", "untitled") that should be inferred from their content.

For each column with a meaningless name, suggest a more meaningful column name based on the data values and detected type.
Also suggest better data types if you think the automatic detection is wrong.

Respond in JSON format:
{{
  "inferred_columns": [
    {{
      "original_name": "col1",
      "inferred_name": "Customer Age",
      "reasoning": "Values range from 18-65 representing customer ages"
    }}
  ]
}}

Only include columns that have meaningless names. Keep the names short (2-4 words max)."""

    return prompt


def parse_inference_response(response_content: str) -> list[dict]:
    import json

    try:
        data = json.loads(response_content)
        return data.get("inferred_columns", [])
    except json.JSONDecodeError:
        return []
