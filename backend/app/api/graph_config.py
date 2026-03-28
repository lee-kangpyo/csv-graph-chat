from typing import Literal, Any

DEFAULT_COLORS = ["#aa3bff", "#10b981", "#f59e0b", "#ef4444", "#3b82f6"]


def generate_chart_config(
    chart_type: Literal["line", "bar", "pie", "scatter", "heatmap", "sankey", "sunburst"],
    labels: list[str],
    series_data: list,
    title: str = None,
    x_axis_label: str = None,
    y_axis_label: str = None,
) -> dict:
    config: dict = {
        "title": {"text": title} if title else {},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": [y_axis_label or "data"]} if chart_type != "pie" else {},
    }

    if chart_type in ["line", "bar", "scatter"]:
        config["xAxis"] = {
            "type": "category",
            "data": labels,
            "name": x_axis_label or "",
        }
        config["yAxis"] = {
            "type": "value",
            "name": y_axis_label or "",
        }
        config["series"] = [{
            "type": chart_type,
            "data": series_data,
            "itemStyle": {"color": DEFAULT_COLORS[0]},
        }]
        if chart_type == "line":
            config["series"][0]["smooth"] = True

    elif chart_type == "pie":
        config["series"] = [{
            "type": "pie",
            "radius": "50%",
            "data": [{"value": v, "name": l} for l, v in zip(labels, series_data)],
        }]

    elif chart_type == "heatmap":
        config["xAxis"] = {"type": "category", "data": labels}
        config["yAxis"] = {"type": "category", "data": labels}
        config["visualMap"] = {"min": 0, "max": max(series_data) if series_data else 100}
        config["series"] = [{"type": "heatmap", "data": series_data}]

    elif chart_type == "sankey":
        config["series"] = [{
            "type": "sankey",
            "layout": "none",
            "data": [{"name": l} for l in labels],
            "links": series_data,
        }]

    elif chart_type == "sunburst":
        config["series"] = [{
            "type": "sunburst",
            "data": series_data,
        }]

    return config


def format_data_for_chart(
    rows: list,
    x_key: str,
    y_key: str,
    chart_type: Literal["line", "bar", "pie", "scatter", "heatmap", "sankey", "sunburst"],
) -> tuple[list[str], list]:
    labels = []
    values = []

    for row in rows:
        if isinstance(row, dict):
            labels.append(str(row.get(x_key, "")))
            values.append(float(row.get(y_key, 0)))
        else:
            labels.append(str(row[0] if len(row) > 0 else ""))
            values.append(float(row[1] if len(row) > 1 else 0))

    if chart_type == "scatter":
        return labels, [[x, y] for x, y in zip(range(len(values)), values)]

    return labels, values


def generate_graph_config_from_sql_result(
    sql_result: list,
    x_column: str,
    y_column: str,
    chart_type: Literal["line", "bar", "pie", "scatter", "heatmap", "sankey", "sunburst"],
) -> dict:
    labels, series_data = format_data_for_chart(sql_result, x_column, y_column, chart_type)

    return generate_chart_config(
        chart_type=chart_type,
        labels=labels,
        series_data=series_data,
        title=f"{y_column} by {x_column}",
        x_axis_label=x_column,
        y_axis_label=y_column,
    )


def generate_echarts_config_from_llm(
    chart_type: str,
    data: list,
    title: str = None,
    x_axis_name: str = None,
    y_axis_name: str = None,
) -> dict:
    config: dict = {
        "title": {"text": title} if title else {},
        "tooltip": {"trigger": "axis"},
    }

    if chart_type in ["line", "bar"]:
        config["xAxis"] = {"type": "category", "data": data.get("x", [])}
        config["yAxis"] = {"type": "value", "name": y_axis_name or ""}
        config["series"] = [{"type": chart_type, "data": data.get("y", [])}]

    elif chart_type == "pie":
        config["series"] = [{
            "type": "pie",
            "radius": "50%",
            "data": [{"value": v, "name": n} for n, v in zip(data.get("names", []), data.get("values", []))],
        }]

    return config
