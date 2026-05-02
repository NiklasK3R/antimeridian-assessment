def antimeridian(lon1: float, lon2: float) -> tuple[bool, float]:
    """
    Determines if a path between two coordinates crosses the antimeridian,
    meaning the difference between longitudes is larger than 180°.
    """
    difference = abs(lon1 - lon2)
    intersect = difference > 180
    return intersect, difference
