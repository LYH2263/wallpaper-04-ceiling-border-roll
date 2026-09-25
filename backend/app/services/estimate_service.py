from fastapi import HTTPException

from app.engines.wallpaper_math import roll_count
from app.modules.ceiling_border import CEILING_BORDER_USABLE_M, ceiling_border_rolls
from app.repositories import history, rolls, settings_repo, walls


def run_estimate(
    wall_id: int,
    roll_id: int,
    save: bool,
    note: str,
    ceiling_on: bool = False,
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

    # 墙面订货卷数：与顶线完全独立，关顶线时结果与改造前一致。
    calc = roll_count(
        wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
    )

    # 入参缺省时合并默认值：角数取墙面默认，段长取设置页默认。
    resolved_corners = corners if corners is not None else wall.get("corner_count")
    resolved_segment = (
        segment_len if segment_len is not None else settings_repo.get_ceiling_segment_len()
    )

    ceiling = {"on": bool(ceiling_on), "usable_len_m": CEILING_BORDER_USABLE_M}
    if not ceiling_on:
        ceiling.update({"rolls": 0, "corners": None, "segment_len_m": None})
    else:
        # 预览只回包（含错误标记、不落库）；确认时非法参数拒绝写入历史。
        try:
            cb = ceiling_border_rolls(resolved_corners, resolved_segment, CEILING_BORDER_USABLE_M)
            ceiling.update(
                {
                    "rolls": cb["rolls"],
                    "corners": cb["corners"],
                    "segment_len_m": cb["segment_len_m"],
                    "total_len_m": cb["total_len_m"],
                    "error": None,
                }
            )
        except (TypeError, ValueError) as exc:
            if save:
                raise HTTPException(400, f"invalid ceiling border input: {exc}")
            ceiling.update(
                {
                    "rolls": None,
                    "corners": resolved_corners,
                    "segment_len_m": resolved_segment,
                    "error": str(exc),
                }
            )

    result = {**calc, "wall_id": wall_id, "roll_id": roll_id, "ceiling": ceiling}
    run_id = None
    if save:
        # 写入时钉住墙面卷数、顶线卷数、角数、段长与开关；历史不再随默认值重算。
        run_id = history.insert_run(wall_id, roll_id, result, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **calc, "ceiling": ceiling}
