from typing import Literal, Any

DEFAULT_COLORS = ["#aa3bff", "#10b981", "#f59e0b", "#ef4444", "#3b82f6"]


def generate_chart_config(
    chart_type: Literal["line", "bar", "doughnut", "scatter"],
    labels: list[str],
    datasets: list[dict],
    title: str = None,
    x_axis_label: str = None,
    y_axis_label: str = None,
) -> dict:
    config = {
        "type": chart_type,
        "data": {"labels": labels, "datasets": datasets},
        "options": {
            "responsive": True,
            "plugins": {"legend": {"display": True, "position": "top"}},
        },
    }

    if title:
        config["options"]["plugins"]["title"] = {"display": True, "text": title}

    if chart_type in ["line", "bar"]:
        config["options"]["scales"] = {
            "x": {
                "display": True,
                "title": {"display": bool(x_axis_label), "text": x_axis_label or ""},
            },
            "y": {
                "display": True,
                "title": {"display": bool(y_axis_label), "text": y_axis_label or ""},
            },
        }

    return config


def format_datasets_for_chart(
    rows: list, x_key: str, y_key: str, chart_type: str
) -> tuple[list[str], list[dict]]:
    labels = []
    values = []

    for row in rows:
        if isinstance(row, dict):
            labels.append(str(row.get(x_key, "")))
            values.append(float(row.get(y_key, 0)))
        else:
            labels.append(str(row[0] if len(row) > 0 else ""))
            values.append(float(row[1] if len(row) > 1 else 0))

    dataset = {
        "label": y_key,
        "data": values,
        "backgroundColor": DEFAULT_COLORS[0] if chart_type == "bar" else DEFAULT_COLORS,
        "borderColor": DEFAULT_COLORS[0]
        if chart_type != "doughnut"
        else DEFAULT_COLORS,
        "fill": False,
    }

    if chart_type == "line":
        dataset["tension"] = 0.1
    elif chart_type == "doughnut":
        dataset["backgroundColor"] = DEFAULT_COLORS[: len(values)]

    return labels, [dataset]


def generate_graph_config_from_sql_result(
    sql_result: list,
    x_column: str,
    y_column: str,
    chart_type: Literal["line", "bar", "doughnut", "scatter"],
) -> dict:
    labels, datasets = format_datasets_for_chart(
        sql_result, x_column, y_column, chart_type
    )

    return generate_chart_config(
        chart_type=chart_type,
        labels=labels,
        datasets=datasets,
        title=f"{y_column} by {x_column}",
        x_axis_label=x_column,
        y_axis_label=y_column,
    )
