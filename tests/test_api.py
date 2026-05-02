from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.mark.parametrize("lon1, lat1, lon2, lat2, crosses_expected, diff_expected", [
    (170.5, 45.0, -175.3, 50.2, True, 345.8),   #Assesment task example
    (15.4, 52.9, 10.0, 29.8, False, 5.4),       #Does not cross the antimeridian
    (-100.0, 34.9, 100.0, 67.8, True, 200.0),    #Another antimeridian cross
    (180.0, 28.0, -180.0, 87.9, True, 360)      #In our logic this should be consideres as a crossing
])
def test_antimeridian_cases(lon1, lat1, lon2, lat2, crosses_expected, diff_expected):
    response = client.post("/api/check-antimeridian", json={"point1": {"type": "Point", "coordinates": [lon1, lat1]},
                                                            "point2": {"type": "Point", "coordinates": [lon2, lat2]}
    })

    assert response.status_code == 200
    data = response.json()

    assert data["crosses_antimeridian"] == crosses_expected
    assert data["longitude_difference"] == pytest.approx(diff_expected, abs=0.1)


@pytest.mark.parametrize("lon1, lat1, lon2, lat2", [
    (180.5, 45.0, -175.3, 90.2),    #Not a valid coordinate input
    (-190.9, 0.9, 178.3, 23.4),
    (24.0, 130.8, 27.9, 91.7),
    (45.0, 170.5, 50.2, -175.3)
])
def test_antimeridian_invalid_input(lon1, lat1, lon2, lat2):
    response = client.post("/api/check-antimeridian", json={"point1": {"type": "Point", "coordinates": [lon1, lat1]},
                                                            "point2": {"type": "Point", "coordinates": [lon2, lat2]}
    })

    assert response.status_code == 422


def test_antimeridian_empty_input():
    response = client.post("/api/check-antimeridian", json={})
    assert response.status_code == 422

def test_antimeridian_wrong_type():
    response = client.post("/api/check-antimeridian", json={"point1": {"type": "Coordinates", "coordinates": [170.4, 45.7, -175.0, 63.3]},
                                                           "point2": {"type": "Coordinates", "coordinates": [10.0, 10.0, 10.0, 10.0]}
    })
    assert response.status_code == 422
