from fastapi import FastAPI
from app.structures import AntimeridianRequest, AntimeridianResponse, PointOutput
from app.logic import antimeridian

app = FastAPI(
    title="Antimeridian Crossing Check",
    description="Determines if a satellite path between two points crosses the antimeridian.",
    version="1.0.0",
)


@app.post("/api/check-antimeridian", response_model=AntimeridianResponse)
def check_antimeridian(request: AntimeridianRequest) -> AntimeridianResponse:
    """
    Checks if a path between two geographical points crosses the antimeridian
    (line at 180° (or -180°) longitude)
    """
    lon1, lat1 = request.point1.coordinates
    lon2, lat2 = request.point2.coordinates

    intersect, difference = antimeridian(lon1, lon2)

    return AntimeridianResponse(
        point1=PointOutput(longitude=lon1, latitude=lat1),
        point2=PointOutput(longitude=lon2, latitude=lat2),
        crosses_antimeridian=intersect,
        longitude_difference=round(difference, 1),
    )
