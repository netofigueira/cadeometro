from src.buildings.building import Building


class BuildGetterQuintoAndar:

    def __init__(self):
        self.url = "https://www.quintoandar.com.br/imovel/"

    def get_building_url(self, building: Building) -> str:
        return self.url + str(building._id)
