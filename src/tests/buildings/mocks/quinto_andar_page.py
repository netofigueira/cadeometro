import os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "quinto-andar-building.html"), "r") as file:
    mock_quinto_andar_building_page = file.read()