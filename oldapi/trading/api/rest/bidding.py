from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from trading.api.context import HTTPContext


router = APIRouter(
    prefix="/bid"
)

@router.get("/")
async def bid_info(
    ctx: HTTPContext = Depends(),
) -> dict[str, str]:
    return {
        "message": "Hello, World!",
    }
