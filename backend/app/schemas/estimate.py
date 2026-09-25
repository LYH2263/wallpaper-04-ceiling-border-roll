from typing import Optional

from pydantic import BaseModel


class EstimateRequest(BaseModel):
    wall_id: int
    roll_id: int
    save: bool = False
    note: str = ""
    border_enabled: bool = False
    corners: Optional[int] = None
    segment_len: Optional[float] = None
