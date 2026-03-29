import json
import os
import logging
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..api.llm_client import LLMClient
from ..api.insight_recommendation import (
    generate_insight_prompt,
    generate_chart_prompt,
    parse_analysis_intent,
    get_fallback_intent,
)
from ..api.graph_config import generate_chart_config
from ..api.pandas_processor import load_csv_data, process_analysis_intent

router = APIRouter(prefix="/api/chat", tags=["chat"])

CHART_KEYWORDS = ["차트", "그래프", "그려", "시각화", "chart", "graph", "plot", "visualize"]


def detect_chart_request(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CHART_KEYWORDS)


def generate_chart_from_file(message: str, csv_metadata: dict) -> Optional[dict]:
    """file_id로 CSV를 직접 읽어 LLM intent 분석 후 chart config 생성"""
    logger.info(f"[CHART] generate_chart_from_file 시작 - message: {message}")
    
    if not csv_metadata:
        logger.warning("[CHART] csv_metadata가 None")
        return None

    file_id = csv_metadata.get("file_id")
    if not file_id:
        logger.warning("[CHART] file_id 없음")
        return None

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "uploads", f"{file_id}.csv"
    )
    logger.info(f"[CHART] 파일 경로: {file_path}")
    
    if not os.path.exists(file_path):
        logger.warning(f"[CHART] 파일 없음: {file_path}")
        return None

    try:
        logger.info("[CHART] CSV 파일 로드 중...")
        df = load_csv_data(file_path)
        sample_data = df.head(10).to_dict(orient="records")
        columns = csv_metadata.get("columns", [])
        row_count = csv_metadata.get("row_count", len(df))
        logger.info(f"[CHART] CSV 로드 완료 - rows: {len(df)}, columns: {[c.get('name') for c in columns]}")

        logger.info("[CHART] LLM에 intent 분석 요청...")
        llm = LLMClient.get_instance()
        prompt = generate_chart_prompt(
            columns=columns,
            row_count=row_count,
            user_request=message,
            sample_data=sample_data,
        )

        response = llm.chat(
            messages=[{"role": "user", "content": prompt}], stream=False
        )
        response_content = response.choices[0].message.content if response.choices else ""
        logger.info(f"[CHART] LLM 응답: {response_content[:200] if response_content else 'empty'}...")

        intent = parse_analysis_intent(response_content)
        logger.info(f"[CHART] 파싱된 intent: {intent}")

        if intent is None:
            logger.info("[CHART] intent 파싱 실패, fallback 시도...")
            intent = get_fallback_intent(columns, message, sample_data)
            logger.info(f"[CHART] fallback intent: {intent}")

        if intent is None:
            logger.warning("[CHART] intent 최종 실패 - graph null 반환")
            return None

        logger.info(f"[CHART] pandas 처리 시작: {intent}")
        result = process_analysis_intent(df, intent)

        if result is None:
            logger.warning("[CHART] pandas 처리 결과 null")
            return None

        logger.info("[CHART] chart config 생성 완료")
        return generate_chart_config(
            chart_type=result["chart_type"],
            labels=result["labels"],
            series_data=result["values"],
            title=result.get("title"),
            x_axis_label=result.get("x_axis_label"),
            y_axis_label=result.get("y_axis_label"),
        )

    except Exception as e:
        logger.error(f"[CHART] 예외 발생: {e}")
        return None


class ChatRequest(BaseModel):
    message: str
    csv_metadata: Optional[dict] = None


async def generate_chat_response(message: str, csv_metadata: Optional[dict] = None):
    llm = LLMClient.get_instance()

    messages = []

    if csv_metadata:
        prompt = generate_insight_prompt(
            columns=csv_metadata.get("columns", []),
            row_count=csv_metadata.get("row_count", 0),
            user_question=message,
        )
        messages.append({"role": "system", "content": prompt})

    messages.append({"role": "user", "content": message})

    response = llm.chat(messages=messages, stream=True)

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield {
                "event": "message",
                "data": json.dumps(
                    {"content": chunk.choices[0].delta.content, "graph": None}
                ),
            }

    graph = None
    if detect_chart_request(message):
        graph = generate_chart_from_file(message, csv_metadata)

    yield {"event": "done", "data": json.dumps({"done": True, "graph": graph})}


@router.post("/stream")
async def chat_stream(request: Request):
    body = await request.json()
    message = body.get("message", "")
    csv_metadata = body.get("csv_metadata")

    return EventSourceResponse(generate_chat_response(message, csv_metadata))


@router.post("/")
async def chat(request: ChatRequest):
    llm = LLMClient.get_instance()

    messages = []

    if request.csv_metadata:
        prompt = generate_insight_prompt(
            columns=request.csv_metadata.get("columns", []),
            row_count=request.csv_metadata.get("row_count", 0),
            user_question=request.message,
        )
        messages.append({"role": "system", "content": prompt})

    messages.append({"role": "user", "content": request.message})

    response = llm.chat(messages=messages, stream=False)

    content = response.choices[0].message.content if response.choices else ""

    graph = None
    if detect_chart_request(request.message):
        graph = generate_chart_from_file(request.message, request.csv_metadata)

    return {"content": content, "graph": graph}
