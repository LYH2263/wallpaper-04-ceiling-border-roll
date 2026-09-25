from typing import Optional

from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service

router = APIRouter()


@router.get("/estimate")
def estimate_get(
    wall_id: int = Query(...),
    roll_id: int = Query(...),
    save: bool = False,
    border_enabled: bool = False,
    corners: Optional[int] = None,
    segment_len: Optional[float] = None,
):
    return estimate_service.run_estimate(wall_id, roll_id, save, "", border_enabled, corners, segment_len)


@router.post("/estimate")
def estimate_post(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.wall_id,
        body.roll_id,
        body.save,
        body.note,
        body.border_enabled,
        body.corners,
        body.segment_len,
    )
