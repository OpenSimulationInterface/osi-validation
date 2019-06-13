"""
Module that contain OSIDataContainer class to handle and manager OSI scenarios
"""

import osi3.osi_sensorview_pb2
import osi3.osi_groundtruth_pb2
import osi3.osi_sensordata_pb2


class OSIDataContainer:
    """This class wrap OSI data. It can import and decode OSI scenarios."""

    def __init__(self):
        self.data = list()
        self._text_data = ""

    # Open and Read text file

    def _read_text_data(self, file_name):
        """ Read data from file """
        with open(file_name, "rb") as text_file:
            data = text_file.read()
        self._text_data = data

    # Search for separators
    def _separate_all_sections(self, start=0, end=0):
        """ Separate files based on  """
        encoded = self._text_data

        separator = b'$$__$$'

        is_finished = False
        while not is_finished:
            end = encoded.find(separator, start)

            # Finishing coverage
            if end == -1:
                is_finished = True
                end = len(encoded)

            if not encoded[start:end]:
                break
            yield encoded[start:end]
            start = end + len(separator)

    # Decode Protobuf data
    def _decode_data(self, encoded_data, data_class):
        """ Decoder osi binary data into provided OSI class
        Input:
        - encoded_data - byte type data
        - osi class to be parsed
        """
        decoded_data = []
        for row in encoded_data:
            data_object = data_class()
            data_object.ParseFromString(row)
            decoded_data.append(data_object)
        self.data = decoded_data

    def from_file(self, path, message_t_name):
        """Import a scenario from a file"""
        message_types = {
            "SensorView": osi3.osi_sensorview_pb2.SensorView,
            "GroundTruth": osi3.osi_groundtruth_pb2.GroundTruth,
            "SensorData": osi3.osi_sensordata_pb2.SensorData
        }

        data_class = message_types[message_t_name]

        self._read_text_data(path)
        generator_separator = self._separate_all_sections()
        self._decode_data(generator_separator, data_class)

        print(f'Data file {path} contained {len(self.data)} timestamps.')

    def get_data(self, timestamp):
        """Get the message of specified timestamp in handled data"""
        return self.data[timestamp]
