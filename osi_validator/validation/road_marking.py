#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging 

#Related third party imports.
import osi3.osi_roadmarking_pb2

#Local application specific imports.
import validation.common

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value

from validation.traffic_sign import TrafficSignValueValidator


# Names of loggers in the module
MODULE_LOGGER_NAME         = 'v_osi.road_marking'
ROAD_MARKING_VALIDATOR_LOGGER_NAME = 'v_osi.road_marking.RoadMarkingValidator'
ROAD_MARKING_CLASSIFICATION_VALIDATOR_LOGGER_NAME = 'v_osi.road_marking.RoadMarkingClassificationValidator'

# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

class RoadMarkingValidator:
    
    def __init__(self):
        self.log = logging.getLogger(ROAD_MARKING_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data   


    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data = osi3.osi_roadmarking_pb2.RoadMarking()
        data.ParseFromString(encoded_data)
        self.load_data(data)

    def validate(self):
        """ Validate  """
        self.log.debug(f'Cheking osi3::RoadMarking object in context "{self.context}"')
        reault_a = self._check_id()
        reault_b = self._check_base()
        result_c = self._check_classification()
        return reault_a and reault_b and result_c

    def _check_base(self):
        """ Check the base of road moraking"""
        base_validator = validation.common.BaseStationaryValidator()
        base_validator.load_data(self._data.base)
        return base_validator.validate()

    def _check_id(self):
        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        return id_validator.validate()

    def _check_classification(self):
        classification_validator = RoadMarkingClassificationValidator()
        classification_validator.load_data(self._data.classification)
        return classification_validator.validate()

class RoadMarkingClassificationValidator:

    def __init__(self):
        self.log = logging.getLogger(ROAD_MARKING_CLASSIFICATION_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data   

    def validate(self):
        """ Validate  """

        result_type = self._check_type()

        # If road marking is a trafic sign 
        traffic_sign_types = ['TYPE_PAINTED_TRAFFIC_SIGN','TYPE_SYMBOLIC_TRAFFIC_SIGN','TYPE_TEXTUAL_TRAFFIC_SIGN']
        if result_type in traffic_sign_types:
            result_ms_type = self._check_ms_type() # traffic_main_sign_type        
            
            if result_type == 'TYPE_TEXTUAL_TRAFFIC_SIGN':
                result_value_text = self._check_value_text()
    
        # Does not influence final result 
        result_ms_type = self._check_monochrome_color() # monochrome_color
        
        # Does not influence final result 
        result_value = self._check_value()

        if result_type == 'TYPE_TEXTUAL_TRAFFIC_SIGN':
            result_value_text = self._check_value_text()
    
        result_assigned_lane_id = self._check_assigned_lane_id()

        return bool(result_type) and result_assigned_lane_id

    def _check_type(self):
        if not is_set(self._data, 'type'):
            self.log.warning('The field "type" is not present in RoadMarking.Classification')
            return False
        else:
            self.log.debug(f'Field classification.type has value of '
                           f'({self._data.type})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_roadmarking_pb2.RoadMarking.Classification.Type
        type_name = get_enum_name(enum_wrapper, self._data.type)
        self.log.debug(f'Lane.Classification.type name is set to "{type_name}"')
        return str(type_name)  

    def _check_ms_type(self):
        if not is_set(self._data, 'traffic_main_sign_type'):
            self.log.warning('The field "traffic_main_sign_type" is not present in RoadMarking.Classification')
            return False
        else:
            self.log.debug(f'Field classification.traffic_main_sign_type has value of ({self._data.type})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_trafficsign_pb2.TrafficSign.MainSign.Classification.Type

        type_name = get_enum_name(enum_wrapper, self._data.traffic_main_sign_type)
        self.log.debug(f'Lane.Classification.traffic_main_sign_type name is set to "{type_name}"')
        return str(type_name)  

    def _check_monochrome_color(self):
        if not is_set(self._data, 'monochrome_color'):
            self.log.warning('The field "monochrome_color" is not present in RoadMarking.Classification')
            return False
        else:
            self.log.debug(f'Field classification.monochrome_color has value of '
                           f'({self._data.monochrome_color})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_roadmarking_pb2.RoadMarking.Classification.Color
        type_name = get_enum_name(enum_wrapper, self._data.monochrome_color)
        self.log.debug(f'Lane.Classification.monochrome_color name is set to "{type_name}"')
        return str(type_name)

    def _check_value(self):
        if not is_set(self._data, 'value'):
            self.log.warning('The field "value" is not present in RoadMarking.Classification')
            return False
        else:
            self.log.debug(f'Field classification.value has value of '
                           f'({self._data.value})')

        tsv = TrafficSignValueValidator()
        tsv.load_data(self._data.value)
        return tsv.validate()

    def _check_value_text(self):
        if not is_set(self._data, 'value_text'):
            self.log.warning('The field "value_text" is not present in RoadMarking.Classification')
            return False
        else:
            self.log.debug(f'Field classification.value_text has value of '
                           f'({self._data.value_text})')

    def _check_assigned_lane_id(self):
        """ Check if the field is set and all the values are present"""

        if is_iterable_set(self._data, 'assigned_lane_id') is False:
            self.log.warning(f'Field assigned_lane_id is not set in RoadMarking.Classification')
            return False

        ids = self._data.assigned_lane_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid
