from typing import Optional

from pydantic import BaseModel


class EstimateRequest(BaseModel):
    wall_id: int
    roll_id: int
    save: bool = False
    note: str = ""
    # 顶线（腰卷）开关与入参；关闭时墙面 rolls 与改造前完全相同。
    ceiling_on: bool = False
    corners: Optional[int] = None
    segment_len: Optional[float] = None
