from fastapi import HTTPException

from app.engines.wallpaper_math import roll_count
from app.modules.ceiling_border import border_roll_count
from app.repositories import history, rolls, settings_repo, walls

DEFAULT_BORDER_SEGMENT_LEN = 0.5


def _resolve_segment_len(segment_len):
    if segment_len is not None:
        return float(segment_len)
    raw = settings_repo.get_all().get("border_segment_len")
    try:
        return float(raw)
    except (TypeError, ValueError):
        return DEFAULT_BORDER_SEGMENT_LEN


def run_estimate(
    wall_id: int,
    roll_id: int,
    save: bool,
    note: str,
    border_enabled: bool = False,
    corners: int | None = None,
    segment_len: float | None = None,
):
    wall = walls.get_wall(wall_id)
    if not wall:
        raise HTTPException(404, "wall not found")
    roll = rolls.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if wall.get("data_quality") == "dirty" or roll.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty seed entity")

    try:
        calc = roll_count(
            wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
        )
    except ValueError as e:
        raise HTTPException(422, str(e))

    border = {
        "enabled": bool(border_enabled),
        "corners": int(corners) if corners is not None else int(wall.get("corners") or 0),
        "segment_len_m": round(_resolve_segment_len(segment_len), 3),
        "effective_len_m": roll["length"],
        "rolls": 0,
    }
    if border_enabled:
        try:
            border.update(
                border_roll_count(border["corners"], border["segment_len_m"], roll["length"])
            )
        except ValueError as e:
            raise HTTPException(422, f"border invalid: {e}")

    result = {**calc, "border": border}
    run_id = None
    if save:
        run_id = history.insert_run(wall_id, roll_id, {**result, "wall_id": wall_id, "roll_id": roll_id}, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **result}
