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
        title=f"{x_column}별 {y_column}",
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


def generate_chart_config_from_result(result: dict) -> dict:
    """pandas_processor에서 반환된 result_data를 기반으로 ECharts config를 생성합니다."""
    chart_type = result.get("chart_type", "bar")
    title = result.get("title", "")
    
    config = {
        "title": {"text": title},
        "tooltip": {"trigger": "item" if chart_type in ["pie", "sankey", "sunburst"] else "axis"},
        "legend": {}
    }

    if chart_type in ["scatter", "scatter_visualmap"]:
        config["xAxis"] = {"type": "value", "name": result.get("x_axis_label", "X")}
        config["yAxis"] = {"type": "value", "name": result.get("y_axis_label", "Y")}
        series_item = {
            "type": "scatter",
            "data": result.get("scatter_data", [])
        }
        if chart_type == "scatter_visualmap" and len(result.get("columns", [])) > 1:
            # We can map visual map or dimensions if a category is present
            config["visualMap"] = {
                "min": 0, "max": 5, # Fallback, should calculate actual range
                "dimension": 1,
                "orient": "horizontal", "right": 10, "top": "top"
            }
        config["series"] = [series_item]

    elif chart_type == "heatmap":
        config["xAxis"] = {"type": "category", "data": result.get("labels", []), "splitArea": {"show": True}}
        config["yAxis"] = {"type": "category", "data": result.get("y_labels", []), "splitArea": {"show": True}}
        config["visualMap"] = {
            "min": 0,
            "max": max([v[2] for v in result.get("heatmap_data", [])]) if result.get("heatmap_data") else 100,
            "calculable": True, "orient": "horizontal", "left": "center", "bottom": "15%"
        }
        config["series"] = [{"name": "Heatmap", "type": "heatmap", "data": result.get("heatmap_data", []), "label": {"show": True}}]

    elif chart_type == "sankey":
        config["series"] = [{
            "type": "sankey",
            "layout": "none",
            "emphasis": {"focus": "adjacency"},
            "data": result.get("nodes", []),
            "links": result.get("links", []),
        }]

    elif chart_type == "boxplot":
        config["xAxis"] = {"type": "category", "data": result.get("labels", [])}
        config["yAxis"] = {"type": "value"}
        # ECharts boxplot needs prepareBoxplotData explicitly or format data [min, Q1, median, Q3, max]
        # For simplicity, passing raw data as "box_data" requires 'boxplot' dataset transformation in ECharts,
        # but here we generate standard structures. Real dataset transformations often happen on frontend,
        # but since we send JSON, we'll embed the raw data to be transformed by frontend or just let ECharts dataset handle it.
        config["dataset"] = [
            {"source": result.get("box_data", [])},
            {"transform": {"type": "boxplot"}}
        ]
        config["series"] = [{"name": "boxplot", "type": "boxplot", "datasetIndex": 1}]

    elif chart_type in ["stacked_bar", "dual_axis"]:
        config["legend"]["data"] = result.get("legend", [])
        config["xAxis"] = {"type": "category", "data": result.get("labels", [])}
        
        if chart_type == "dual_axis":
            config["yAxis"] = [
                {"type": "value", "name": "Value 1"},
                {"type": "value", "name": "Value 2"}
            ]
        else:
            config["yAxis"] = {"type": "value"}

        series = []
        for i, (name, data) in enumerate(result.get("series_dict", {}).items()):
            s = {
                "name": name,
                "type": "bar" if chart_type == "stacked_bar" else ("line" if i % 2 == 1 else "bar"),
                "data": data
            }
            if chart_type == "stacked_bar":
                s["stack"] = "total"
            if chart_type == "dual_axis" and i % 2 == 1:
                s["yAxisIndex"] = 1
            series.append(s)
        config["series"] = series

    elif chart_type == "radar":
        # Radar charts require 'indicator' [{name, max}] array
        legend = result.get("legend", [])
        labels = result.get("labels", [])
        series_dict = result.get("series_dict", {})
        
        indicators = [{"name": l, "max": max([series_dict[lg][i] for lg in legend]) if legend else 100} for i, l in enumerate(labels)]
        config["radar"] = {"indicator": indicators}
        
        radar_data = []
        for name, data in series_dict.items():
            radar_data.append({"value": data, "name": name})
            
        config["legend"]["data"] = legend
        config["series"] = [{"name": "Radar", "type": "radar", "data": radar_data}]

    else:
        # Fallback for simple bar, line, pie
        config["xAxis"] = {"type": "category", "data": result.get("labels", [])}
        config["yAxis"] = {"type": "value", "name": result.get("y_axis_label", "")}
        config["series"] = [{
            "type": chart_type,
            "data": result.get("values", []),
            "itemStyle": {"color": DEFAULT_COLORS[0]}
        }]
        if chart_type == "pie":
            del config["xAxis"]
            del config["yAxis"]
            config["series"] = [{
                "type": "pie",
                "radius": "50%",
                "data": [{"value": v, "name": l} for l, v in zip(result.get("labels", []), result.get("values", []))]
            }]
        if chart_type == "line":
            config["series"][0]["smooth"] = True

    return config
