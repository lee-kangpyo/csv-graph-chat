from pydantic import BaseModel
from typing import Optional, Literal


class ColumnMetadata(BaseModel):
    name: str
    inferred_name: Optional[str] = None
    data_type: Literal["date", "number", "category", "boolean", "unknown"] = "unknown"
    sample_values: list[str] = []


class CSVMetadata(BaseModel):
    file_name: str
    table_name: str
    columns: list[ColumnMetadata]
    row_count: int


class GraphAxisConfig(BaseModel):
    x: str
    y: str


class GraphStyleConfig(BaseModel):
    colors: list[str] = ["#aa3bff", "#10b981", "#f59e0b", "#ef4444", "#3b82f6"]
    title: Optional[str] = None


class GraphConfig(BaseModel):
    type: Literal["line", "bar", "doughnut", "scatter"]
    title: Optional[str] = None
    x_axis: str
    y_axis: str
    labels: list[str] = []
    datasets: list[dict] = []
    style: GraphStyleConfig = GraphStyleConfig()


class BasketItem(BaseModel):
    id: str
    name: str
    graph_config: GraphConfig
    created_at: str
