import logging
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..api.chat import generate_chart_from_file

router = APIRouter(prefix="/api/chart", tags=["chart"])


class ChartGenerateRequest(BaseModel):
    message: str
    csv_metadata: Optional[dict] = None
    request_id: Optional[str] = None


class ChartGenerateResponse(BaseModel):
    request_id: Optional[str] = None
    graph: Optional[dict] = None


@router.post("/generate")
async def generate_chart(request: ChartGenerateRequest):
    logger.info(f"[CHART] /api/chart/generate 호출 - request_id: {request.request_id}")

    if not request.message:
        return ChartGenerateResponse(request_id=request.request_id, graph=None)

    graph = generate_chart_from_file(request.message, request.csv_metadata)

    return ChartGenerateResponse(request_id=request.request_id, graph=graph)
