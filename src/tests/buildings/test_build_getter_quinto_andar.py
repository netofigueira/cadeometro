import unittest
from unittest import mock

from src.buildings.build_getter_quinto_andar import BuildGetterQuintoAndar
from src.buildings.building import Building


class TestBuildGetterQuintoAndar(unittest.TestCase):
    def test_get_building_url(self):
        getter = BuildGetterQuintoAndar()
        test_building = Building(1, 20.0, 30.5)

        test_url = getter.get_building_url(test_building)
        expected_reponse = getter.url + "1"

        self.assertEqual(test_url, expected_reponse)
