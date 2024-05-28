import unittest
from unittest import mock

from src.buildings.build_lister_quinto_andar import BuildListerQuintoAndar
from src.buildings.building import Building


class TestBuildListerQuintoAndar(unittest.TestCase):
    def test_get_buildings(self):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"location": "example"}

        bounds = {
            "cent_lat": -23.28,
            "cent_lon": -23.28,
            "bounds_north": -23.28,
            "bounds_south": -23.82,
            "bounds_east": -46.43,
            "bounds_west": -46.84,
            "min_value": 100,
            "max_value": 1000,
        }

        lister = BuildListerQuintoAndar()
        with unittest.mock.patch("requests.get") as mocked_get:
            mocked_get.return_value = mock_response
            response = lister._get_buildings(**bounds)
            mocked_get.assert_called_once()
            assert response == mock_response.json()

    @mock.patch(
        "src.buildings.build_lister_quinto_andar"
        ".BuildListerQuintoAndar._get_buildings"
    )
    def test_get_building_list(self, mocked_response):
        mocked_response.return_value = {
            "hits": {
                "hits": [
                    {
                        "_id": 1,
                        "_source": {"location": {"lat": 20.0, "lon": 30.5}},
                    }
                ]
            }
        }

        bounds = {
            "cent_lat": -23.28,
            "cent_lon": -23.28,
            "bounds_north": -23.28,
            "bounds_south": -23.82,
            "bounds_east": -46.43,
            "bounds_west": -46.84,
            "min_value": 100,
            "max_value": 1000,
        }

        lister = BuildListerQuintoAndar()

        response = lister.get_building_list(**bounds)
        expected_response = [Building(1, 20.0, 30.5)]

        self.assertListEqual(expected_response, response)

    @mock.patch(
        "src.buildings.build_lister_quinto_andar"
        ".BuildListerQuintoAndar._get_buildings"
    )
    def test_get_buildings_close(self, mocked_response):
        mocked_response.return_value = {
            "hits": {
                "hits": [
                    {
                        "_id": 1,
                        "_source": {"location": {"lat": 20.0, "lon": 30.5}},
                    }
                ]
            }
        }
        lister = BuildListerQuintoAndar()

        response = lister.get_buildings_close(20.0, 30.5)
        expected_response = [Building(1, 20.0, 30.5)]

        self.assertListEqual(expected_response, response)
