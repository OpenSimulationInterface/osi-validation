"""Module for test class of OSIValidationRules class"""

import sys
import unittest
from osivalidator import osi_data_container

sys.path.append("..")


class TestDataContainer(unittest.TestCase):
    """Test class of OSIDataContainer class"""

    def test_import(self):
        """Test the importation of a OSI message"""
        odc = osi_data_container.OSIDataContainer()
        odc.set_message_type("SensorView")
        odc.from_file(
            "tests/overtake_right_straight_SensorView.txt",
            show_progress=False,
            show_exec_time=False)

    def test_get_message_by_index(self):
        odc = osi_data_container.OSIDataContainer()
        odc.set_message_type("SensorView")
        odc.from_file(
            "tests/overtake_right_straight_SensorView.txt", "SensorView",
            show_progress=False,
            show_exec_time=False)
        for index in range(500):
            odc.get_message_by_index(index)

    def test_get_messages_in_index_range(self):
        odc = osi_data_container.OSIDataContainer()
        odc.from_file(
            "tests/overtake_right_straight_SensorView.txt", "SensorView",
            show_progress=False,
            show_exec_time=False)
        for _ in odc.get_messages_in_index_range(0, 500):
            pass

    def test_cache_messages(self):
        odc = osi_data_container.OSIDataContainer()
        odc.from_file(
            "tests/overtake_right_straight_SensorView.txt", "SensorView",
            show_progress=False,
            show_exec_time=False)
        odc.cache_messages_in_index_range(0, 500)

    def test_accessing_cache_messages(self):
        odc = osi_data_container.OSIDataContainer()
        odc.from_file(
            "tests/overtake_right_straight_SensorView.txt", "SensorView",
            show_progress=False,
            show_exec_time=False)
        odc.cache_messages_in_index_range(0, 500)

        for index in range(500):
            odc.get_message_by_index(index)
