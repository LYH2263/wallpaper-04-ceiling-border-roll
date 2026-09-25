import pytest

from app.modules.ceiling_border import CEILING_BORDER_USABLE_M, ceiling_border_rolls


def test_less_than_one_roll_rounds_up():
    # 4 角 × 0.5m = 2m，不足一卷仍向上取整为 1 卷。
    r = ceiling_border_rolls(4, 0.5)
    assert r["total_len_m"] == 2.0
    assert r["rolls"] == 1


def test_exact_multiple_no_over_round():
    assert ceiling_border_rolls(20, 1.0)["rolls"] == 2


def test_partial_roll_rounds_up():
    # 21m / 10m = 2.1 → 3 卷。
    assert ceiling_border_rolls(21, 1.0)["rolls"] == 3


def test_uses_configured_usable_length():
    assert ceiling_border_rolls(8, 1.0, usable_len=4.0)["rolls"] == 2
    assert CEILING_BORDER_USABLE_M == 10.0


@pytest.mark.parametrize("corners,seg,usable", [
    (0, 0.5, 10.0),
    (-3, 0.5, 10.0),
    (4, 0.0, 10.0),
    (4, -0.5, 10.0),
    (4, 0.5, 0.0),
    (4, 0.5, -10.0),
])
def test_invalid_inputs_rejected(corners, seg, usable):
    with pytest.raises(ValueError):
        ceiling_border_rolls(corners, seg, usable)
