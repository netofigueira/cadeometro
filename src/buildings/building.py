from dataclasses import dataclass


@dataclass
class Building:
    _id: str = ""
    lat: str = ""
    lon: str = ""


@dataclass
class BuildingPhoto:
    _id: str = ""
    path: str = ""
    url: str = ""
