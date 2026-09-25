from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import walls as repo

router = APIRouter()


class CornersBody(BaseModel):
    corners: int


@router.get("/walls")
def list_walls():
    return {"items": repo.list_walls()}


@router.get("/walls/{wall_id}")
def get_wall(wall_id: int):
    row = repo.get_wall(wall_id)
    if not row:
        raise HTTPException(404)
    return row


@router.post("/walls/{wall_id}/corners")
def set_default_corners(wall_id: int, body: CornersBody):
    """墙面详情存默认角数；角数必须为正。"""
    if body.corners <= 0:
        raise HTTPException(400, "corners must be positive")
    if not repo.update_corner_count(wall_id, body.corners):
        raise HTTPException(404, "wall not found")
    return repo.get_wall(wall_id)
