"""Module for test class of OSIValidationRules class"""

import unittest
from osivalidator.osi_scenario import OSIScenario


class TestDataContainer(unittest.TestCase):
    """Test class of OSIScenario class"""

    def setUp(self):
        self.MESSAGE_LENGTH = 50
        self.odc = OSIScenario()
        self.odc.from_file(path="../osi_message_data/osi_message_test.txt",
                           type_name="SensorView")

    def tearDown(self):
        self.odc.scenario_file.close()
        del self.odc

    def test_get_message_by_index(self):
        for index in range(self.MESSAGE_LENGTH):
            self.odc.get_message_by_index(index)

    def test_get_messages_in_index_range(self):
        for _ in self.odc.get_messages_in_index_range(0, self.MESSAGE_LENGTH):
            pass

    def test_cache_messages(self):
        self.odc.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

    def test_accessing_cache_messages(self):
        self.odc.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

        for index in range(self.MESSAGE_LENGTH):
            self.odc.get_message_by_index(index)
