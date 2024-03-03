from __future__ import annotations

from fastapi import APIRouter

from . import bidding

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(bidding.router)
