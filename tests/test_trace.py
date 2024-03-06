"""Module for test class of OSIValidationRules class"""

import unittest
from osivalidator.osi_trace import OSITrace
import subprocess


class TestDataContainer(unittest.TestCase):
    """Test class of OSITrace class"""

    def setUp(self):
        self.MESSAGE_LENGTH = 10

        self.osi = OSITrace(buffer_size=1000000)
        self.osi_nobuffer = OSITrace(buffer_size=0)

        self.osi.from_file(
            path="data/20240221T141700Z_sv_312_10_one_moving_object.osi",
            type_name="SensorView",
        )
        self.osi_nobuffer.from_file(
            path="data/20240221T141700Z_sv_312_10_one_moving_object.osi",
            type_name="SensorView",
        )

    def tearDown(self):
        self.osi.trace_file.close()
        del self.osi

        self.osi_nobuffer.trace_file.close()
        del self.osi_nobuffer

    def test_get_messages_in_index_range(self):
        """Test getting messages in range"""

        for _ in self.osi.get_messages_in_index_range(0, self.MESSAGE_LENGTH):
            pass

        for _ in self.osi_nobuffer.get_messages_in_index_range(0, self.MESSAGE_LENGTH):
            pass

    def test_get_message_in_index(self):
        """Test getting messages by index"""

        self.osi.get_message_by_index(0)
        self.osi_nobuffer.get_message_by_index(0)

    def test_cache_messages(self):
        """Test caching messages"""

        self.osi.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)
        self.osi_nobuffer.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

    def test_accessing_cache_messages(self):
        """Test accessing of cached messages"""

        self.osi.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

        for index in range(self.MESSAGE_LENGTH):
            self.osi.get_message_by_index(index)

        self.osi_nobuffer.cache_messages_in_index_range(0, self.MESSAGE_LENGTH)

        for index in range(self.MESSAGE_LENGTH):
            self.osi_nobuffer.get_message_by_index(index)
