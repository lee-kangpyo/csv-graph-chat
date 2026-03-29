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
        base_prompt += """

Based on the data structure detected (dates, numbers, or categories), you SHOULD creatively recommend combinations of the following Advanced Chart Insights:
- "분포 및 이상치 분석" (Distribution/Boxplot): Check for risk signals and data spreads.
- "흐름 및 이탈 경로 추적" (Flow/Sankey): Track transitions from a source state to a target state.
- "상관관계 분석" (Correlation/Scatter): Find causal relationships between two numeric columns.
- "밀집도 분석" (Density/Heatmap): Find bottlenecks using two categorical dimensions.
- "혼합 지표 분석" (Dual Axis): Compare cumulative totals alongside percentage rates.
- "시계열 추이" (Time Series Trend/Line): Show trends over time.
- "그룹별 다이내믹 비교" (Group Comparison/Bar/Pie/Radar): Rank values or compare multi-dimensional scores.

Suggest 2-3 specific, actionable analysis questions (e.g. "어느 단과대학에서 학사경고 후 제적되는 흐름이 가장 많은지 산키 다이어그램으로 볼까요?") based on the actual columns provided."""
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

    prompt = f"""You are an advanced data analyst AI. Look at the sample data below and determine the best chart visualization strategy to answer the user request.

CSV columns ({row_count} rows total):
{chr(10).join(column_info)}

Sample data (first 10 rows):
{sample_rows}
User request: "{user_request}"

YOUR TASK: Translate the user's request into a single visualization Intent JSON based on 11 available chart types.

Available Chart Types (`chart_type`):
1. "bar" (group comparisons)
2. "line" (time series/trends)
3. "scatter" (correlations between 2 numerics)
4. "stacked_bar" (component parts across categories)
5. "pie" (proportions)
6. "boxplot" (distributions/outliers)
7. "heatmap" (density across 2 categories)
8. "sankey" (flow/transitions from source to target)
9. "dual_axis" (mixed metrics like bar+line)
10. "scatter_visualmap" (clustering/scatter with boundary colors)
11. "radar" (multi-dimensional assessment)

Rules for the JSON Output Structure:
- You MUST use ONLY this unified schema:
  {{"analysis_type": "advanced_chart", "chart_type": "...", "x_col": "...", "y_col": "...", "category_col": "...", "value_col": "...", "agg_func": "sum/count/mean", "title": "..."}}
- Only use keys: `chart_type`, `x_col`, `y_col`, `category_col`, `value_col`, `agg_func`, `title`.
- Leave fields empty/null if they are not needed for the specific `chart_type`.
- `x_col` is usually the primary axis or category (e.g., date, dept). For Sankey, it's the `source`.
- `y_col` is usually the secondary axis or target category. For Sankey, it's the `target`.
- `value_col` is the numeric column to be aggregated.
- `agg_func` is one of "sum", "count", "mean", "max", "min".
- Pick the most meaningful columns based on the sample data.
- title MUST be in Korean (한글). Do NOT use English titles.

You MUST output ONLY a single JSON object. No explanation. No markdown. No extra text.

Example outputs:
{{"analysis_type": "advanced_chart", "chart_type": "scatter", "x_col": "study_hours", "y_col": "test_score", "category_col": "class", "value_col": null, "agg_func": null, "title": "공부 시간 vs 시험 점수"}}
{{"analysis_type": "advanced_chart", "chart_type": "sankey", "x_col": "college", "y_col": "status", "category_col": null, "value_col": "student_id", "agg_func": "count", "title": "학생 흐름 및 중도탈락"}}

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
        "analysis_type": "advanced_chart",
        "chart_type": chart_type,
        "x_col": group_col,
        "y_col": None,
        "category_col": None,
        "value_col": number_columns[0],
        "agg_func": "mean",
        "title": f"{group_col}별 {number_columns[0]}",
    }
