from typing import List

import requests

from src.buildings.building import Building
from src.buildings.build_lister import BuildLister


class BuildListerQuintoAndar(BuildLister):
    """BuilderLister"""

    def __init__(self):
        self.url = "https://www.quintoandar.com.br/api/yellow-pages/v2/search"

    def _get_buildings(
        self,
        bounds_north: str,
        bounds_south: str,
        bounds_east: str,
        bounds_west: str,
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
            "authority": "www.quintoandar.com.br",
            "accept": "/",
            "accept-language": "en-US,en;q=0.7",
            "cookie": (
                "X-AB-Test=ab_booking_pressure_sale:0,ab_exposed_filter_sale_desktop:1,ab_exposed_filter_sale_v1:0,ab_increase_service_fee:-1,ab_load_more_v0:1,ab_ltr_ranking_experiment_rent:0,ab_profiling_v2:0,ab_property_finding_tests:-1,ab_rebrand_guia:1,ab_scheduling_step_by_step_v1:0,ab_search_for_filters_v1:0;"
                " ab.storage.deviceId.cf9e8c77-7b32-4126-940b-b58658d0918e=%7B%22g%22%3A%2216571f6a-fa7c-8a5f-bc04-aea0ad654fd6%22%2C%22c%22%3A1674583013208%2C%22l%22%3A1674583013208%7D;"
                " ab.storage.sessionId.cf9e8c77-7b32-4126-940b-b58658d0918e=%7B%22g%22%3A%22aff8a628-e7a3-4be7-60c6-ea51c3ebd489%22%2C%22e%22%3A1674584891967%2C%22c%22%3A1674583013207%2C%22l%22%3A1674583091967%7D;"
                " amplitude_id_3fbf25d58c3cce92f0e6609904a37cc9quintoandar.com.br=eyJkZXZpY2VJZCI6ImM1YWRjYTE3LTE2NWYtNDBmMS1iZWE2LTJhZWZiNTUyODlkZFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY3NDU4MzAxMzE5OSwibGFzdEV2ZW50VGltZSI6MTY3NDU4MzEzNjc2NCwiZXZlbnRJZCI6OSwiaWRlbnRpZnlJZCI6NzU4LCJzZXF1ZW5jZU51bWJlciI6NzY3fQ=="
            ),
            "sec-ch-ua": (
                '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,"
                " like Gecko) Chrome/109.0.0.0 Safari/537.36"
            ),
        }
        params = {
            "map[bounds_north]": bounds_north,
            "map[bounds_south]": bounds_south,
            "map[bounds_east]": bounds_east,
            "map[bounds_west]": bounds_west,
            "availability": "any",
            "occupancy": "any",
            "business_context": "RENT",
            "return": "location",
            "photos": 12,
            "relax_query": False,
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
        bounds_north: str,
        bounds_south: str,
        bounds_east: str,
        bounds_west: str,
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
            bounds_north, bounds_south, bounds_east, bounds_west
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
    response = builder._get_buildings(**bounds)
    print(response.keys())
    print(len(response["hits"]["hits"]))
    print(response["hits"]["hits"][0])

    buildings = builder.get_building_list(**bounds)
    print(buildings[0:5])

    buildings_close = builder.get_buildings_close(-23.6440973, -46.5501203)
    print(buildings_close)
