import unittest

from src.buildings.build_getter_quinto_andar import BuildGetterQuintoAndar
from src.buildings.building import Building, BuildingPhoto, BuildingData
from src.tests.buildings.mocks.quinto_andar_page import mock_quinto_andar_building_page


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

    def test_get_building_photos_fallback(self):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = [{"id": "111", "url": "test"}]

        getter = BuildGetterQuintoAndar()
        getter.base_url_photos_list = "teste.com/_building_id_"
        getter.base_url_photos_list_fallback = "testfallb.com/_building_id_"
        with unittest.mock.patch("requests.get") as mocked_get:
            mocked_get.return_value = mock_response
            response = getter.get_buildings_photos(Building("1"))

        self.assertListEqual(
            [
                BuildingPhoto(
                    "111",
                    "test",
                    getter.base_url_photos + "test",
                )
            ],
            response,
        )
        self.assertNotEqual("teste.com/1", getter.url_photo_list)
        self.assertEqual("testfallb.com/1", getter.url_photo_list)

    def test_get_building_basic_data(self):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 400
        mock_response.text = mock_quinto_andar_building_page

        getter = BuildGetterQuintoAndar()
        getter.base_url_photos_list = "teste.com/_building_id_"
        with unittest.mock.patch("requests.get") as mocked_get:
            mocked_get.return_value = mock_response
            response = getter.get_building_basic_data(Building("1"))

        expected_response = BuildingData(
            _id="1",
            type="Apartment",
            name="Casa",
            address="Rua Antonio",
            floor_size=150,
            number_rooms=3,
            principal_images_url=["test.JPG", "test2.JPG"],
            price=100,
            description="description",
        )

        self.assertEqual(expected_response._id, response._id)
        self.assertEqual(expected_response.type, response.type)
        self.assertEqual(expected_response.name, response.name)
        self.assertEqual(expected_response.address, response.address)
        self.assertEqual(expected_response.floor_size, response.floor_size)
        self.assertEqual(expected_response.number_rooms, response.number_rooms)
        self.assertEqual(expected_response.price, response.price)
        self.assertEqual(expected_response.description, response.description)
        self.assertListEqual(
            expected_response.principal_images_url, response.principal_images_url
        )
