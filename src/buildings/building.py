from dataclasses import dataclass


@dataclass
class Building:
    _id: str = ""
    lat: str = ""
    lon: str = ""


@dataclass
class BuildingData:
    _id: str
    type: str
    name: str
    address: str
    floor_size: int
    number_rooms: int
    principal_images_url: list[str]
    price: int
    description: str


@dataclass
class BuildingPhoto:
    _id: str = ""
    path: str = ""
    url: str = ""
