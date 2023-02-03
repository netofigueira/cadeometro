from typing import List

import requests

from src.buildings.building import Building, BuildingPhoto


class BuildGetterQuintoAndar:
    def __init__(self):
        self.url = "https://www.quintoandar.com.br/imovel/"
        self.base_url_photos = "https://www.quintoandar.com.br/img/200x200/"
        self.base_url_photos_list = (
            "https://www.quintoandar.com.br/api/kodak/v1/media"
            "/photo/house/_building_id_/categorized-photos"
        )

    def get_building_url(self, building: Building) -> str:
        return self.url + str(building._id)

    def get_buildings_photos(self, building: Building) -> List[BuildingPhoto]:
        self.url_photo_list = self.base_url_photos_list.replace(
            "_building_id_", building._id
        )
        response = requests.get(self.url_photo_list)

        try:
            response_dict = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Erro")
            response_dict = []

        photos = [
            BuildingPhoto(
                raw_photo["id"],
                raw_photo["path"],
                self.base_url_photos + raw_photo["path"],
            )
            for raw_photo in response_dict
        ]

        return photos


if __name__ == "__main__":
    builder = BuildGetterQuintoAndar()
    response = builder.get_buildings_photos(Building("893252684"))
    print(response)
