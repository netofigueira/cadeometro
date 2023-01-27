from math import radians, degrees
from typing import Tuple


class BuildLister:
    def __init__(self) -> None:
        pass

    def get_building_list(self):
        raise NotImplementedError

    def get_buildings_close(self, lat: str, lon: str) -> list:
        bounds = self._bounding_box(lat, lon)
        return self.get_building_list(*bounds)

    def _bounding_box(
        self, lat: str, lon: str, distance: float = 1.0
    ) -> Tuple[int]:
        # Earth's radius in kilometers
        R = 6371.0

        # Convert distance and original coordinates to radians
        lat_rad = radians(lat)
        lon_rad = radians(lon)
        dist_rad = distance / R

        # Calculate bounding box coordinates
        bounds_south = lat_rad - dist_rad
        bounds_north = lat_rad + dist_rad
        bounds_west = lon_rad - dist_rad
        bounds_east = lon_rad + dist_rad

        # Convert back to degrees
        bounds_south = degrees(bounds_south)
        bounds_north = degrees(bounds_north)
        bounds_west = degrees(bounds_west)
        bounds_east = degrees(bounds_east)

        return (bounds_north, bounds_south, bounds_east, bounds_west)
