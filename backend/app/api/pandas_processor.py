import pandas as pd
from typing import Optional, Literal


def load_csv_data(file_path: str) -> pd.DataFrame:
    """CSV 파일을 pandas DataFrame으로 로드합니다."""
    for encoding in ["utf-8", "euc-kr", "cp949", "latin-1"]:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(file_path, encoding="utf-8", errors="ignore")


def process_group_by(
    df: pd.DataFrame,
    group_by: str,
    value: str,
    agg_func: Literal["mean", "sum", "count", "min", "max"] = "mean",
) -> tuple[list[str], list]:
    """groupby aggregation을 수행합니다."""
    if group_by not in df.columns or value not in df.columns:
        return [], []

    try:
        result = df.groupby(group_by)[value].agg(agg_func)

        if result.empty:
            return [], []

        labels = result.index.astype(str).tolist()
        values = result.values.tolist()

        return labels, values
    except Exception:
        return [], []


def process_time_series(
    df: pd.DataFrame,
    time_col: str,
    value: str,
    freq: Literal["daily", "weekly", "monthly", "quarterly", "yearly"] = "monthly",
) -> tuple[list[str], list]:
    """시계열 데이터 처리 및 리샘플링을 수행합니다."""
    if time_col not in df.columns or value not in df.columns:
        return [], []

    try:
        df_ts = df.copy()
        df_ts[time_col] = pd.to_datetime(df_ts[time_col], errors="coerce")
        df_ts = df_ts.dropna(subset=[time_col])

        if df_ts.empty:
            return [], []

        freq_map = {
            "daily": "D",
            "weekly": "W",
            "monthly": "MS",
            "quarterly": "QS",
            "yearly": "YS",
        }
        grouper_freq = freq_map.get(freq, "MS")

        result = df_ts.groupby(pd.Grouper(key=time_col, freq=grouper_freq))[value].mean()

        if result.empty:
            return [], []

        labels = result.index.astype(str).tolist()
        values = result.values.tolist()

        return labels, values
    except Exception:
        return [], []


def validate_processing_result(labels: list, values: list) -> bool:
    """pandas 처리 결과가 유효한지 검증합니다."""
    if not labels or not values:
        return False
    if len(labels) != len(values):
        return False
    if all(v == 0 or (isinstance(v, float) and pd.isna(v)) for v in values):
        return False
    return True


def process_analysis_intent(df: pd.DataFrame, intent: dict) -> Optional[dict]:
    """분석 intent를 기반으로 데이터 처리를 수행합니다."""
    analysis_type = intent.get("analysis_type")

    if analysis_type == "group_by":
        labels, values = process_group_by(
            df,
            group_by=intent.get("group_by", ""),
            value=intent.get("value", ""),
            agg_func=intent.get("agg_func", "mean"),
        )
    elif analysis_type == "time_series":
        labels, values = process_time_series(
            df,
            time_col=intent.get("time_col", ""),
            value=intent.get("value", ""),
            freq=intent.get("freq", "monthly"),
        )
    else:
        return None

    if not validate_processing_result(labels, values):
        return None

    return {
        "labels": labels,
        "values": values,
        "chart_type": intent.get("chart_type", "bar"),
        "title": intent.get("title", f"{intent.get('value', 'Data')} by {intent.get('group_by', intent.get('time_col', 'Category'))}"),
        "x_axis_label": intent.get("group_by") or intent.get("time_col"),
        "y_axis_label": intent.get("value", ""),
    }
