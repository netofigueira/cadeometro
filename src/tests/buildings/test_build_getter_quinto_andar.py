import unittest

from src.buildings.build_getter_quinto_andar import BuildGetterQuintoAndar
from src.buildings.building import Building, BuildingPhoto


class TestBuildGetterQuintoAndar(unittest.TestCase):
    def test_get_building_url(self):
        getter = BuildGetterQuintoAndar()
        test_building = Building(1, 20.0, 30.5)

        test_url = getter.get_building_url(test_building)
        expected_reponse = getter.url + "1"

        self.assertEqual(test_url, expected_reponse)

    def test_get_building_photos(self):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "111", "path": "test"}]

        getter = BuildGetterQuintoAndar()
        getter.base_url_photos_list = "teste.com/_building_id_"
        with unittest.mock.patch("requests.get") as mocked_get:
            mocked_get.return_value = mock_response
            response = getter.get_buildings_photos(Building("1"))
            mocked_get.assert_called_once()

        self.assertListEqual(
            [BuildingPhoto("111", "test", getter.base_url_photos + "test")],
            response,
        )
        self.assertEqual("teste.com/1", getter.url_photo_list)
