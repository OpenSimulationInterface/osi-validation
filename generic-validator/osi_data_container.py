import osi3.osi_sensorview_pb2


class OsiDataContainer:
    data = list()
    # Open and Read text file

    def _read_text_data(self, file_name):
        """ Read data from file """
        with open(file_name, "rb") as f:
            data = f.read()
        return data

    # Search for separators
    def _separate_all_sections(self, encoded):
        """ Separate files based on  """
        SEPARATOR = b'$$__$$'
        start, end = 0, 0

        is_finished = False
        while not is_finished:
            end = encoded.find(SEPARATOR, start)

            # Finishing coverage
            if end == -1:
                is_finished = True
                end = len(encoded)

            if len(encoded[start:end]) == 0:
                break
            yield encoded[start:end]
            start = end + len(SEPARATOR)

    # Decode protobuff data
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
        return decoded_data

    def from_file(self, path):
        data_class = osi3.osi_sensorview_pb2.SensorView

        binary_data = self._read_text_data(path)
        generator_separator = self._separate_all_sections(binary_data)
        list_of_data = self._decode_data(generator_separator, data_class)

        print(f'Data file {path} contained {len(list_of_data)} timestamps.')

        self.data = list_of_data
