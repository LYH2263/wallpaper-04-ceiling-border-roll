from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories import settings_repo

router = APIRouter()

ALLOWED_KEYS = {"border_segment_len"}


class SettingUpdate(BaseModel):
    key: str
    value: str


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.post("/settings")
def update_setting(body: SettingUpdate):
    if body.key not in ALLOWED_KEYS:
        raise HTTPException(400, "unknown setting")
    try:
        value = float(body.value)
    except (TypeError, ValueError):
        raise HTTPException(422, "value must be a number")
    if value <= 0:
        raise HTTPException(422, "value must be positive")
    settings_repo.set_value(body.key, body.value)
    return settings_repo.get_all()
