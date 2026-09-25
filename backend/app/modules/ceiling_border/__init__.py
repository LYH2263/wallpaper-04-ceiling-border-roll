"""Ceiling border (顶线角段): rolls from corner count × per-corner segment length
divided by the waist roll's effective length, rounded up. Wall rolls are unaffected."""

from app.engines.helpers import ceil_units


def border_roll_count(corners: int, segment_len: float, effective_len: float) -> dict:
    if isinstance(corners, float) and not corners.is_integer():
        raise ValueError("invalid corners")
    corners = int(corners)
    segment_len = float(segment_len)
    effective_len = float(effective_len)
    if corners <= 0:
        raise ValueError("invalid corners")
    if segment_len <= 0:
        raise ValueError("invalid segment length")
    if effective_len <= 0:
        raise ValueError("invalid effective length")
    total_len = corners * segment_len
    return {
        "corners": corners,
        "segment_len_m": round(segment_len, 3),
        "effective_len_m": round(effective_len, 3),
        "total_len_m": round(total_len, 3),
        "rolls": ceil_units(total_len / effective_len),
    }
