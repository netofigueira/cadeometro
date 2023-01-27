import unittest
from unittest import mock

from src.buildings.build_lister import BuildLister
from src.buildings.building import Building


class TestBuildLister(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_bouding_box(self):
        lister = BuildLister()
        north, south, east, west = lister._bounding_box(10.0, 20.3)

        self.assertGreater(north, 10)
        self.assertGreater(10, south)
        self.assertGreater(east, 20.3)
        self.assertGreater(20.3, west)