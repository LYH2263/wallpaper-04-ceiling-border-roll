import pytest

from app.modules.ceiling_border import border_roll_count


def test_border_basic():
    r = border_roll_count(4, 0.5, 10.0)
    assert r["corners"] == 4
    assert r["total_len_m"] == 2.0
    assert r["rolls"] == 1


def test_border_rounds_up():
    r = border_roll_count(4, 2.7, 10.0)
    assert r["total_len_m"] == 10.8
    assert r["rolls"] == 2


def test_border_exact_multiple_not_overcounted():
    assert border_roll_count(4, 2.5, 10.0)["rolls"] == 1
    assert border_roll_count(8, 2.5, 10.0)["rolls"] == 2


def test_border_rejects_nonpositive_corners():
    with pytest.raises(ValueError):
        border_roll_count(0, 0.5, 10.0)
    with pytest.raises(ValueError):
        border_roll_count(-2, 0.5, 10.0)


def test_border_rejects_nonpositive_segment_len():
    with pytest.raises(ValueError):
        border_roll_count(4, 0, 10.0)
    with pytest.raises(ValueError):
        border_roll_count(4, -0.5, 10.0)


def test_border_rejects_nonpositive_effective_len():
    with pytest.raises(ValueError):
        border_roll_count(4, 0.5, 0)
    with pytest.raises(ValueError):
        border_roll_count(4, 0.5, -10.0)
