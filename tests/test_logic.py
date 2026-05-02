from app.logic import antimeridian
import pytest


@pytest.mark.parametrize(
    "l1, l2, expected",
    [
        (170.0, -175.0, (True, 345.0)),
        (180.0, -180.0, (True, 360.0)),
        (120.4, -20.3, (False, 140.7)),
        (0.0, 0.0, (False, 0.0)),
        (-100.0, 100.0, (True, 200.0)),
        (100.0, -100.0, (True, 200.0)),
        (90.0, -90.0, (False, 180.0)),
    ],
)
def test_antimeridian(l1, l2, expected):
    assert antimeridian(l1, l2)[0] == expected[0]
    assert antimeridian(l1, l2)[1] == pytest.approx(expected[1])
