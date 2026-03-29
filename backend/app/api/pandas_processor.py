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


def process_advanced_chart(df: pd.DataFrame, intent: dict) -> Optional[dict]:
    chart_type = intent.get("chart_type", "bar").lower()
    x_col = intent.get("x_col")
    y_col = intent.get("y_col")
    cat_col = intent.get("category_col")
    val_col = intent.get("value_col")
    agg_func = intent.get("agg_func", "mean") or "mean"

    result_data = {}

    try:
        if chart_type in ["scatter", "scatter_visualmap"]:
            if x_col in df.columns and y_col in df.columns:
                cols_to_extract = [x_col, y_col]
                if cat_col and cat_col in df.columns:
                    cols_to_extract.append(cat_col)
                df_clean = df[cols_to_extract].dropna()
                result_data["scatter_data"] = df_clean.values.tolist()
                result_data["columns"] = cols_to_extract
            else:
                return None
                
        elif chart_type == "heatmap":
            if x_col in df.columns and y_col in df.columns and val_col in df.columns:
                grouped = df.groupby([x_col, y_col])[val_col].agg(agg_func).reset_index()
                x_labels = sorted(df[x_col].dropna().unique().tolist())
                y_labels = sorted(df[y_col].dropna().unique().tolist())
                
                heatmap_data = []
                for _, row in grouped.iterrows():
                    try:
                        x_idx = x_labels.index(row[x_col])
                        y_idx = y_labels.index(row[y_col])
                        heatmap_data.append([x_idx, y_idx, row[val_col]])
                    except ValueError:
                        continue
                        
                result_data["labels"] = x_labels
                result_data["y_labels"] = y_labels
                result_data["heatmap_data"] = heatmap_data
            else:
                return None
                
        elif chart_type == "sankey":
            if x_col in df.columns and y_col in df.columns:
                if val_col and val_col in df.columns:
                    grouped = df.groupby([x_col, y_col])[val_col].agg(agg_func).reset_index()
                else:
                    grouped = df.groupby([x_col, y_col]).size().reset_index(name='count')
                    val_col = 'count'
                
                links = []
                nodes_set = set()
                for _, row in grouped.iterrows():
                    src = str(row[x_col])
                    tgt = str(row[y_col])
                    val = float(row[val_col])
                    links.append({"source": src, "target": tgt, "value": val})
                    nodes_set.add(src)
                    nodes_set.add(tgt)
                
                result_data["nodes"] = [{"name": n} for n in nodes_set]
                result_data["links"] = links
            else:
                return None
                
        elif chart_type == "boxplot":
            if x_col in df.columns and y_col in df.columns:
                df_clean = df[[x_col, y_col]].dropna()
                grouped = df_clean.groupby(x_col)[y_col]
                categories = []
                box_data = []
                for name, group in grouped:
                    categories.append(str(name))
                    box_data.append(group.tolist())
                result_data["labels"] = categories
                result_data["box_data"] = box_data
            else:
                return None
                
        elif chart_type in ["stacked_bar", "dual_axis", "radar"]:
            # Needs cross tabulation or pivot
            if x_col in df.columns and val_col in df.columns and cat_col in df.columns:
                pivot = df.pivot_table(index=x_col, columns=cat_col, values=val_col, aggfunc=agg_func, fill_value=0)
                result_data["labels"] = pivot.index.astype(str).tolist()
                series_dict = {}
                for col in pivot.columns:
                    series_dict[str(col)] = pivot[col].tolist()
                result_data["series_dict"] = series_dict
                result_data["legend"] = list(series_dict.keys())
            else:
                return None
                
        else:
            # Fallback simple grouping for bar, line, pie
            if x_col and val_col and x_col in df.columns and val_col in df.columns:
                grouped = df.groupby(x_col)[val_col].agg(agg_func)
                result_data["labels"] = grouped.index.astype(str).tolist()
                result_data["values"] = grouped.values.tolist()
                if not validate_processing_result(result_data["labels"], result_data["values"]):
                    return None
            else:
                return None

        result_data["chart_type"] = chart_type
        result_data["title"] = intent.get("title", f"{x_col or '카테고리'}별 {val_col or '분석'}")
        result_data["x_axis_label"] = x_col
        result_data["y_axis_label"] = y_col or val_col

        return result_data
    except Exception as e:
        print(f"Error process_advanced_chart: {e}")
        return None


def process_analysis_intent(df: pd.DataFrame, intent: dict) -> Optional[dict]:
    """분석 intent를 기반으로 데이터 처리를 수행합니다."""
    analysis_type = intent.get("analysis_type")

    if analysis_type == "advanced_chart":
        return process_advanced_chart(df, intent)
    elif analysis_type == "group_by":
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
        return process_advanced_chart(df, intent)

    if not validate_processing_result(labels, values):
        return None

    return {
        "labels": labels,
        "values": values,
        "chart_type": intent.get("chart_type", "bar"),
        "title": intent.get("title", f"{intent.get('group_by', intent.get('time_col', '카테고리'))}별 {intent.get('value', '데이터')}"),
        "x_axis_label": intent.get("group_by") or intent.get("time_col"),
        "y_axis_label": intent.get("value", ""),
    }
