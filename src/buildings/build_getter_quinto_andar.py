from typing import List
import json
import logging

import requests

from src.buildings.building import Building, BuildingPhoto, BuildingData
from bs4 import BeautifulSoup


class BuildGetterQuintoAndar:
    def __init__(self):
        self.url = "https://www.quintoandar.com.br/imovel/"
        self.base_url_photos = "https://www.quintoandar.com.br/img/200x200/"
        self.base_url_photos_list = (
            "https://www.quintoandar.com.br/api/kodak/v1/media"
            "/photo/house/_building_id_/categorized-photos"
        )
        self.base_url_photos_list_fallback = (
            "https://www.quintoandar.com.br/property/_building_id_/photos?variant=0"
        )
        self.fall_backed = False
        self.path_key = "path"

    def get_building_url(self, building: Building) -> str:
        return self.url + str(building._id)

    def get_building_basic_data(self, building: Building) -> BuildingData:
        url = self.get_building_url(building=building)
        basic_data = self._get_basic_data_dict(url=url)
        basic_data["id"] = building._id
        building_data = self._process_basic_data(basic_data)
        return building_data

    def get_buildings_photos(self, building: Building) -> List[BuildingPhoto]:
        response = self._get_url_with_building(building._id)

        try:
            response_dict = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Erro => {response}, {self.url_photo_list}")
            response_dict = []

        if self.fall_backed:
            self.path_key = "url"
        photos = [
            BuildingPhoto(
                raw_photo["id"],
                raw_photo[self.path_key],
                self.base_url_photos + raw_photo[self.path_key],
            )
            for raw_photo in response_dict
        ]

        return photos

    def _get_basic_data_dict(self, url: str) -> dict:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        script_tags = soup.find_all("script")
        for tag in script_tags:
            if "price" in tag.text:
                correct_tag = tag.text
                break

        response = correct_tag.replace("\xa0", " ")
        try:
            response_dict = json.loads(response)
        except Exception:
            logging.exception("error loading response json")
            response_dict = {}

        return response_dict

    def _process_basic_data(self, basic_data: dict) -> BuildingData:
        object_data: dict = basic_data.get("object")
        return BuildingData(
            _id=basic_data.get("id"),
            type=object_data.get("@type"),
            name=object_data.get("name"),
            address=object_data.get("address"),
            floor_size=object_data.get("floorSize"),
            number_rooms=object_data.get("numberOfRooms"),
            principal_images_url=object_data.get("image"),
            price=basic_data.get("price"),
            description=object_data.get("description"),
        )

    def _get_url_with_building(self, building_id: str):
        self.url_photo_list = self.base_url_photos_list.replace(
            "_building_id_", building_id
        )
        response = requests.get(self.url_photo_list)

        if response.status_code == 200:
            return response

        self.fall_backed = True
        headers = {
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,"
                " like Gecko) Chrome/109.0.0.0 Safari/537.36"
            ),
        }

        self.url_photo_list = self.base_url_photos_list_fallback.replace(
            "_building_id_", building_id
        )
        response = requests.get(self.url_photo_list, headers=headers)

        return response


if __name__ == "__main__":
    builder = BuildGetterQuintoAndar()
    response = builder.get_buildings_photos(Building("893252684"))
    print(response)

    builder = BuildGetterQuintoAndar()
    response = builder.get_buildings_photos(Building("893571237"))
    print(response)

    builder = BuildGetterQuintoAndar()
    response = builder.get_building_basic_data(Building("893571237"))
    print(response)
