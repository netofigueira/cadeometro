from typing import List

import requests

from src.buildings.building import Building
from src.buildings.build_lister import BuildLister


class BuildListerQuintoAndar(BuildLister):
    """BuilderLister"""

    def __init__(self):
        self.url = "https://apigw.prod.quintoandar.com.br/cached/house-listing-search/v1/search/coordinates"

    def _get_buildings(
        self,
        cent_lat: str,
        cent_lon: str,
        bounds_north: str,
        bounds_south: str,
        bounds_east: str,
        bounds_west: str,
        min_price: float,
        max_price: float,
    ) -> dict:
        """_get_buildings.

        Args:
            bounds_north (str): bounds_north
            bounds_south (str): bounds_south
            bounds_east (str): bounds_east
            bounds_west (str): bounds_west

        Returns:
            dict:
        """
        headers = {
            "sec-ch-ua": '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": "",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Linux"',
        }
        params = {
            "context.mapShowing": "false",
            "context.listShowing": "false",
            "context.deviceId": "zPism9Kr9zpqYjSlxC-Um8NZfDQAAGisJPbUuxZWinMXfa9YJJ68Jg",
            "context.numPhotos": "12",
            "context.isSSR": "false",
            "filters.businessContext": "RENT",
            "filters.location.coordinate.lat": cent_lat,
            "filters.location.coordinate.lng": cent_lon,
            "filters.location.viewport.east": bounds_east,
            "filters.location.viewport.north": bounds_north,
            "filters.location.viewport.south": bounds_south,
            "filters.location.viewport.west": bounds_west,
            "filters.location.countryCode": "BR",
            "filters.priceRange[0].costType": "TOTAL_COST",
            "filters.priceRange[0].range.min": str(min_price),
            "filters.priceRange[0].range.max": str(max_price),
            "filters.houseSpecs.houseTypes[0]": "APARTMENT",
            "filters.availability": "ANY",
            "filters.occupancy": "ANY",
            "fields[0]": "location",
            "experiments[0]": "ab_search_services_mono_pclick:0",
            "filters.houseSpecs.bathrooms.range.min": "1",
        }
        response = requests.get(self.url, headers=headers, params=params)

        try:
            response_dict = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Erro")
            response_dict = dict()
        return response_dict

    def get_building_list(
        self,
        cent_lat: str,
        cent_lon: str,
        bounds_north: str,
        bounds_south: str,
        bounds_east: str,
        bounds_west: str,
        min_price: float,
        max_price: float,
    ) -> List[Building]:
        """get_building_list.

        Args:
            bounds_north (str): bounds_north
            bounds_south (str): bounds_south
            bounds_east (str): bounds_east
            bounds_west (str): bounds_west

        Returns:
            List[Building]:
        """
        response_dict = self._get_buildings(
            cent_lat,
            cent_lon,
            bounds_north,
            bounds_south,
            bounds_east,
            bounds_west,
            min_price,
            max_price,
        )
        response_list = response_dict["hits"]["hits"]
        building_list = [
            Building(
                _id=item["_id"],
                lat=item["_source"]["location"]["lat"],
                lon=item["_source"]["location"]["lon"],
            )
            for item in response_list
        ]
        return building_list


if __name__ == "__main__":
    builder = BuildListerQuintoAndar()
    bounds = {
        "bounds_north": -23.282,
        "bounds_south": -23.822,
        "bounds_east": -46.432,
        "bounds_west": -46.842,
    }

    buildings_close = builder.get_buildings_close(-23.6440973, -46.5501203)
    print(buildings_close, end="\n\n---------------\n\n")
    print(len(buildings_close), end="\n\n---------------\n\n")
