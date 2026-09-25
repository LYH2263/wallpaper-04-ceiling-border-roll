from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.repositories import walls as repo

router = APIRouter()


class WallCornersUpdate(BaseModel):
    corners: int = Field(..., ge=0)


@router.get("/walls")
def list_walls():
    return {"items": repo.list_walls()}


@router.get("/walls/{wall_id}")
def get_wall(wall_id: int):
    row = repo.get_wall(wall_id)
    if not row:
        raise HTTPException(404)
    return row


@router.post("/walls/{wall_id}")
def update_wall_corners(wall_id: int, body: WallCornersUpdate):
    if not repo.get_wall(wall_id):
        raise HTTPException(404)
    repo.update_corners(wall_id, body.corners)
    return repo.get_wall(wall_id)
