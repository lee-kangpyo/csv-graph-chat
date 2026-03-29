import json
import re
from typing import Optional


def detect_data_type_combinations(columns: list[dict]) -> dict:
    has_date = any(col.get("data_type") == "date" for col in columns)
    has_number = any(col.get("data_type") == "number" for col in columns)
    has_category = any(col.get("data_type") == "category" for col in columns)
    return {
        "has_date_and_number": has_date and has_number,
        "has_category_and_number": has_category and has_number,
    }


def generate_insight_prompt(
    columns: list[dict], row_count: int, user_question: str = None, sample_data: list = None
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

    sample_data_info = ""
    if sample_data:
        sample_data_info = "\n\nHere are sample rows from the data:\n"
        for i, row in enumerate(sample_data[:10]):
            sample_data_info += f"Row {i+1}: {row}\n" 

    type_combos = detect_data_type_combinations(columns)

    base_prompt = f"""You are a data analyst AI. A user has uploaded a CSV file with {row_count} rows and the following columns:

{chr(10).join(column_info)}
{sample_data_info}

The user wants to understand their data and generate insights."""

    if not user_question:
        if type_combos["has_date_and_number"]:
            base_prompt += """

Based on the data structure (Date + Number columns detected), you SHOULD recommend:
- "시계열 추이" (Time Series Trend): Show trends over time with line charts
  - Offer options: monthly comparison, quarterly comparison, yearly comparison
- Example questions to ask: "월별 매출 추이를 보고 싶으신가요?" or "분기별 트렌드는 어떠세요?"

If the user asks about trends, use time-based grouping (daily/weekly/monthly/quarterly/yearly)."""
        elif type_combos["has_category_and_number"]:
            base_prompt += """

Based on the data structure (Category + Number columns detected), you SHOULD recommend:
- "그룹별 비교" (Group Comparison): Compare values across categories using bar/pie charts
  - Offer options: horizontal bar for ranking, pie chart for proportion
- Example questions to ask: "지역별 매출 비교를 보고 싶으신가요?" or "어떤 카테고리가 가장 큰 비중인가요?"

If the user asks about comparisons, use GROUP BY for aggregation."""
        else:
            base_prompt += """

Ask the user what kind of insights they want, or suggest 2-3 potential analyses based on the data types detected."""
    else:
        base_prompt += f"""

The user specifically asked: "{user_question}"
"""

    base_prompt += """

Provide a helpful, conversational response that guides the user toward actionable insights."""

    return base_prompt


def generate_chart_prompt(
    columns: list[dict], row_count: int, user_request: str, sample_data: list
) -> str:
    column_info = []
    for col in columns:
        col_info = f"- {col['name']}"
        if col.get("sample_values"):
            samples = ", ".join([str(v) for v in col["sample_values"][:3]])
            col_info += f" [e.g., {samples}]"
        column_info.append(col_info)

    sample_rows = ""
    for i, row in enumerate(sample_data[:10]):
        sample_rows += f"  {i+1}. {row}\n"

    prompt = f"""You are a data analyst. Look at the sample data below and determine how to visualize it.

CSV columns ({row_count} rows total):
{chr(10).join(column_info)}

Sample data (first 10 rows):
{sample_rows}
User request: "{user_request}"

YOUR TASK: Identify the best group_by or time_series analysis for this request.

Rules:
- Look at the actual sample values to understand each column's type (number, category, date)
- Pick the most meaningful category/group column for group_by
- Pick the most meaningful numeric column to aggregate

You MUST output ONLY a single JSON object. No explanation. No markdown. No extra text.

Example outputs:
{{"analysis_type": "group_by", "group_by": "학과", "value": "평점", "agg_func": "mean", "chart_type": "bar", "title": "학과별 평균 평점"}}
{{"analysis_type": "time_series", "time_col": "날짜", "value": "매출", "freq": "monthly", "chart_type": "line", "title": "월별 매출 추이"}}

Output the JSON now:"""

    return prompt


def parse_analysis_intent(response_content: str) -> Optional[dict]:
    """LLM 응답에서 분석 intent JSON을 파싱합니다."""
    if not response_content:
        return None

    text = response_content.strip()

    # 마크다운 코드블록 제거
    text = re.sub(r"```(?:json)?\s*", "", text).strip()

    # JSON 객체 추출 시도
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    for match in re.finditer(json_pattern, text):
        try:
            intent = json.loads(match.group(0))
            if isinstance(intent, dict) and "analysis_type" in intent:
                return intent
        except json.JSONDecodeError:
            continue

    # 전체 텍스트를 JSON으로 파싱 시도
    try:
        intent = json.loads(text)
        if isinstance(intent, dict) and "analysis_type" in intent:
            return intent
    except json.JSONDecodeError:
        pass

    return None


def infer_column_types_from_sample(
    columns: list[dict], sample_data: list
) -> tuple[list[str], list[str]]:
    """sample_data 실제 값으로 컬럼 타입을 추론합니다."""
    if not sample_data or not columns:
        return [], []

    number_columns = []
    category_columns = []

    for col in columns:
        col_name = col.get("name")
        if not col_name:
            continue

        values = [row.get(col_name) for row in sample_data[:10] if row.get(col_name) is not None]
        if not values:
            continue

        numeric_count = 0
        for v in values:
            try:
                float(str(v).replace(",", ""))
                numeric_count += 1
            except (ValueError, TypeError):
                pass

        if numeric_count >= len(values) * 0.8:
            number_columns.append(col_name)
        else:
            category_columns.append(col_name)

    return number_columns, category_columns


def get_fallback_intent(
    columns: list[dict], user_request: str = None, sample_data: list = None
) -> Optional[dict]:
    """LLM 파싱 실패 시 sample_data 기반으로 기본 분석 intent를 생성합니다."""
    number_columns = [col["name"] for col in columns if col.get("data_type") == "number"]
    category_columns = [col["name"] for col in columns if col.get("data_type") == "category"]

    # data_type이 unknown인 경우 sample_data로 추론
    if (not number_columns or not category_columns) and sample_data:
        inferred_numbers, inferred_categories = infer_column_types_from_sample(
            columns, sample_data
        )
        if not number_columns:
            number_columns = inferred_numbers
        if not category_columns:
            category_columns = inferred_categories

    if not number_columns:
        return None

    chart_type = "bar"
    if user_request:
        user_lower = user_request.lower()
        if any(k in user_lower for k in ["월별", "날짜", "trend", "시계열", "추이"]):
            chart_type = "line"
        elif any(k in user_lower for k in ["비율", "pie", "파이"]):
            chart_type = "pie"
        elif any(k in user_lower for k in ["산점", "scatter"]):
            chart_type = "scatter"

    group_col = category_columns[0] if category_columns else (columns[0]["name"] if columns else "")

    return {
        "analysis_type": "group_by",
        "group_by": group_col,
        "value": number_columns[0],
        "agg_func": "mean",
        "chart_type": chart_type,
        "title": f"{number_columns[0]} by {group_col}",
    }
