from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import settings_repo

router = APIRouter()


class SegmentBody(BaseModel):
    segment_len: float


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.post("/settings/ceiling-segment")
def set_ceiling_segment(body: SegmentBody):
    """设置页存默认每角段长；必须为正，事后修改不重算旧单。"""
    if body.segment_len <= 0:
        raise HTTPException(400, "segment length must be positive")
    settings_repo.upsert(settings_repo.CEILING_SEGMENT_KEY, body.segment_len)
    return settings_repo.get_all()
