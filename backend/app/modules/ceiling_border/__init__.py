"""顶线（腰卷）开卷：墙角数 × 每角段长 ÷ 腰卷有效长度，向上取整得到顶线卷数。

与墙面订货卷数相互独立、分列计算；本模块只产出顶线卷数，不影响墙面 rolls。
"""

from app.engines.helpers import ceil_units

# 腰卷有效长度（米）：一卷腰卷可实际用于顶线的长度。
CEILING_BORDER_USABLE_M = 10.0


def ceiling_border_rolls(
    corners: float,
    segment_len: float,
    usable_len: float = CEILING_BORDER_USABLE_M,
) -> dict:
    """按 墙角数×每角段长÷有效长度 向上取整计算顶线卷数。

    角数必须为正；段长与有效长度必须 > 0，否则视为非法参数拒绝计算。
    """
    corners = float(corners)
    segment_len = float(segment_len)
    usable_len = float(usable_len)
    if corners <= 0:
        raise ValueError("corners must be positive")
    if segment_len <= 0:
        raise ValueError("segment length must be positive")
    if usable_len <= 0:
        raise ValueError("usable length must be positive")

    total_len = corners * segment_len
    rolls = ceil_units(total_len / usable_len)
    return {
        "corners": int(corners) if corners.is_integer() else corners,
        "segment_len_m": round(segment_len, 3),
        "usable_len_m": round(usable_len, 3),
        "total_len_m": round(total_len, 3),
        "rolls": rolls,
    }
