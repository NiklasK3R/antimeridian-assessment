from pydantic import BaseModel, field_validator


class GeoPoint(BaseModel):
    type: str
    coordinates: list[float]

    @field_validator("type")
    @classmethod
    def validate_type(cls, p):
        if p != "Point":
            raise ValueError(f"Type has to be 'Point' '{p}'")
        return p

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, cords):
        if len(cords) != 2:
            raise ValueError(
                "Coordinates have to consist of only two values [longitude, latitude]"
            )

        lon, lat = cords

        if not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude has to be between -180 and 180")

        if not (-90.0 <= lat <= 90):
            raise ValueError("Latitude has to be between -90 and 90")
        return cords


class AntimeridianRequest(BaseModel):
    point1: GeoPoint
    point2: GeoPoint


class PointOutput(BaseModel):
    longitude: float
    latitude: float


class AntimeridianResponse(BaseModel):
    point1: PointOutput
    point2: PointOutput
    crosses_antimeridian: bool
    longitude_difference: float
