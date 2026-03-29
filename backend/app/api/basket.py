from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from ..db.basket_db import create_basket, get_basket, get_all_baskets, delete_basket

router = APIRouter(prefix="/api/basket", tags=["basket"])


class CreateBasketRequest(BaseModel):
    name: str
    graph_config: dict
    question: str = ''


class BasketResponse(BaseModel):
    id: str
    name: str
    graph_config: dict
    created_at: str
    question: str = ''


@router.post("/", response_model=BasketResponse)
async def create(request: CreateBasketRequest):
    basket_id = str(uuid.uuid4())
    basket = create_basket(basket_id, request.name, request.graph_config, request.question)
    return basket


@router.get("/", response_model=list[BasketResponse])
async def list_baskets():
    return get_all_baskets()


@router.get("/{basket_id}", response_model=BasketResponse)
async def get(basket_id: str):
    basket = get_basket(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    return basket


@router.delete("/{basket_id}")
async def delete(basket_id: str):
    deleted = delete_basket(basket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Basket not found")
    return {"message": "Basket deleted"}
