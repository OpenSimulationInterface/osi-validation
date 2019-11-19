"""
Module that contains OSIDataContainer class to handle and manage OSI scenarios.
"""
from collections import deque
import time
from multiprocessing import Manager
import lzma
import struct

from progress.bar import Bar
from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_sensordata_pb2 import SensorData
import warnings
warnings.simplefilter('default')

from osivalidator.linked_proto_field import LinkedProtoField

SEPARATOR = b'$$__$$'
SEPARATOR_LENGTH = len(SEPARATOR)
BUFFER_SIZE = 1000000


def get_size_from_file_stream(file_object):
    """
    Return a file size from a file stream given in parameters
    """
    current_position = file_object.tell()
    file_object.seek(0, 2)
    size = file_object.tell()
    file_object.seek(current_position)
    return size


MESSAGES_TYPE = {
    "SensorView": SensorView,
    "GroundTruth": GroundTruth,
    "SensorData": SensorData
}


class OSIScenario:
    """This class wrap OSI data. It can import and decode OSI scenarios."""

    def __init__(self, show_progress=True, path=None, type_name="SensorView"):
        self.scenario_file = None
        self.message_offsets = None
        self.type_name = type_name
        self.manager = Manager()
        self.message_cache = self.manager.dict()
        self.timestep_count = 0
        self.show_progress = show_progress
        self.retrieved_scenario_size = 0

        if path is not None and type_name is not None:
            self.from_file(path)

    # Open and Read text file

    def from_file(self, path, type_name="SensorView", max_index=-1, format_type=None):
        """Import a scenario from a file"""
        if path.lower().endswith(('.lzma', '.xz')):
            self.scenario_file = lzma.open(path, "rb")
        else:
            self.scenario_file = open(path, "rb")

        self.type_name = type_name
        self.format_type = format_type

        if self.format_type == 'separated':
            warnings.warn("The separated trace files will be completely removed in the near future. Please convert them to *.osi files with the converter in the main OSI repository.", PendingDeprecationWarning)
            self.timestep_count = self.retrieve_message_offsets(max_index)
        else:
            self.timestep_count = self.retrieve_message()

    def retrieve_message(self):
        scenario_size = get_size_from_file_stream(self.scenario_file)

        max_index = float('inf')

        if self.show_progress:
            progress_bar = Bar(max=scenario_size)
            print("Retrieving message offsets in scenario file until " +
                  str(max_index) + " ...")
        else:
            progress_bar = None

        buffer_deque = deque(maxlen=2)

        self.message_offsets = [0]
        eof = False

        if self.show_progress:
            start_time = time.time()

        self.scenario_file.seek(0)
        serialized_message = self.scenario_file.read()
        INT_LENGTH = len(struct.pack("L", 0))
        message_length = 0

        i = 0
        while i < len(serialized_message):
            message = MESSAGES_TYPE[self.type_name]()
            message_length = struct.unpack("L", serialized_message[i:INT_LENGTH+i])[0]
            message.ParseFromString(serialized_message[i+INT_LENGTH:i+INT_LENGTH+message_length])
            i += message_length + INT_LENGTH
            self.message_offsets.append(message)
            self.update_bar(progress_bar, i)

        if eof:
            self.retrieved_scenario_size = scenario_size
        else:
            self.retrieved_scenario_size = self.message_offsets[-1]
            self.message_offsets.pop()

        if self.show_progress:
            progress_bar.finish()
            print(len(self.message_offsets), "messages has been discovered in",
                  time.time() - start_time, "s")

        return len(self.message_offsets)

    def retrieve_message_offsets(self, max_index):
        """
        Retrieve the offsets of all the messages of the scenario and store them
        in the `message_offsets` attribute of the object

        It returns the number of discovered timesteps
        """
        scenario_size = get_size_from_file_stream(self.scenario_file)

        if max_index == -1:
            max_index = float('inf')

        if self.show_progress:
            progress_bar = Bar(max=scenario_size)
            print("Retrieving message offsets in scenario file until " +
                  str(max_index) + " ...")
        else:
            progress_bar = None

        buffer_deque = deque(maxlen=2)

        self.message_offsets = [0]
        eof = False

        if self.show_progress:
            start_time = time.time()

        self.scenario_file.seek(0)

        while not eof and len(self.message_offsets) <= max_index:
            found = -1  # SEP offset in buffer
            buffer_deque.clear()

            while found == -1 and not eof:
                new_read = self.scenario_file.read(BUFFER_SIZE)
                buffer_deque.append(new_read)
                buffer = b"".join(buffer_deque)
                found = buffer.find(SEPARATOR)
                eof = len(new_read) != BUFFER_SIZE

            buffer_offset = self.scenario_file.tell() - len(buffer)
            message_offset = found + buffer_offset + SEPARATOR_LENGTH
            self.message_offsets.append(message_offset)

            self.update_bar(progress_bar, message_offset)

            self.scenario_file.seek(message_offset)

            while eof and found != -1:
                buffer = buffer[found + SEPARATOR_LENGTH:]
                found = buffer.find(SEPARATOR)

                buffer_offset = scenario_size - len(buffer)

                message_offset = found + buffer_offset + SEPARATOR_LENGTH

                if message_offset >= scenario_size:
                    break
                self.message_offsets.append(message_offset)

                self.update_bar(progress_bar, message_offset)

        if eof:
            self.retrieved_scenario_size = scenario_size
        else:
            self.retrieved_scenario_size = self.message_offsets[-1]
            self.message_offsets.pop()

        if self.show_progress:
            progress_bar.finish()
            print(len(self.message_offsets), "messages has been discovered in",
                  time.time() - start_time, "s")

        return len(self.message_offsets)

    def get_message_by_index(self, index):
        """
        Get a message by its index. Try first to get it from the cache made
        by the method ``cache_messages_in_index_range``.
        """
        message = self.message_cache.get(index, None)

        if message is not None:
            return message

        message = next(self.get_messages_in_index_range(index, index+1))
        return LinkedProtoField(message, name=self.type_name)

    def get_messages_in_index_range(self, begin, end):
        """
        Yield an iterator over messages of indexes between begin and end included.
        """
        if self.show_progress:
            progress_bar = Bar(max=end-begin)
            print("Importing messages from scenario file...")
        else:
            progress_bar = None


        if self.format_type  == 'separated':
            self.scenario_file.seek(self.message_offsets[begin])
            abs_first_offset = self.message_offsets[begin]
            abs_last_offset = self.message_offsets[end] \
                if end < len(self.message_offsets) \
                else self.retrieved_scenario_size

            rel_message_offsets = [
                abs_message_offset - abs_first_offset
                for abs_message_offset in self.message_offsets[begin:end]
            ]

            message_sequence_len = abs_last_offset - \
                abs_first_offset - SEPARATOR_LENGTH
            serialized_messages_extract = self.scenario_file.read(
                message_sequence_len)

            for rel_index, rel_message_offset in enumerate(rel_message_offsets):
                rel_begin = rel_message_offset
                rel_end = rel_message_offsets[rel_index + 1] - SEPARATOR_LENGTH \
                    if rel_index + 1 < len(rel_message_offsets) \
                    else message_sequence_len
                message = MESSAGES_TYPE[self.type_name]()
                serialized_message = serialized_messages_extract[rel_begin:rel_end]
                message.ParseFromString(serialized_message)
                self.update_bar(progress_bar, rel_index)
                yield LinkedProtoField(message, name=self.type_name)

        elif self.format_type is None:
            self.scenario_file.seek(0)
            serialized_message = self.scenario_file.read()
            INT_LENGTH = len(struct.pack("L", 0))
            message_length = 0

            i = 0
            while i < len(serialized_message):
                message = MESSAGES_TYPE[self.type_name]()
                message_length = struct.unpack("L", serialized_message[i:INT_LENGTH+i])[0]
                message.ParseFromString(serialized_message[i+INT_LENGTH:i+INT_LENGTH+message_length])
                i += message_length + INT_LENGTH
                self.update_bar(progress_bar, i)
                yield LinkedProtoField(message, name=self.type_name)

        else:
            raise Exception(f"The defined format {self.format_type} does not exist.")

        if self.show_progress:
            self.update_bar(progress_bar, progress_bar.max)
            progress_bar.finish()

    def cache_messages_in_index_range(self, begin, end):
        """
        Put all messages from index begin to index end in the cache. Then the
        method ``get_message_by_index`` can access to it in a faster way.

        Using this method again clear the last cache and replace it with a new
        one.
        """
        if self.show_progress:
            print('Caching...')
        self.message_cache = self.manager.dict({
            index + begin: message
            for index, message
            in enumerate(self.get_messages_in_index_range(begin, end))
        })
        if self.show_progress:
            print('Caching done!')

    def update_bar(self, progress_bar, new_index):
        if self.show_progress and progress_bar is not None:
            progress_bar.index = new_index
            progress_bar.update()
