"""Module for test class of OSIValidationRules class"""

import unittest
from osivalidator.osi_trace import OSITrace


class TestDataContainer(unittest.TestCase):
    """Test class of OSITrace class"""

    def setUp(self):
        self.MESSAGE_LENGTH = 15
        self.odc = OSITrace()
        self.odc.from_file(path="data/small_test.txt.lzma",
                           type_name="SensorView", format_type='separated')

    def tearDown(self):
        self.odc.trace_file.close()
        del self.odc

    def test_get_messages_in_index_range(self):
        for _ in self.odc.get_messages_in_index_range(0, self.MESSAGE_LENGTH):
            pass

    def test_get_message_in_index(self):
        self.odc.get_message_by_index(0)

    def test_cache_messages(self):
        self.odc.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

    def test_accessing_cache_messages(self):
        self.odc.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

        for index in range(self.MESSAGE_LENGTH):
            self.odc.get_message_by_index(index)
