#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging

#Related third party imports.
import osi3.osi_trafficlight_pb2

#Local application specific imports.
import validation.common

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value


# Names of loggers in the module
MODULE_LOGGER_NAME         = 'v_osi.trafficlight'
TRAFFIC_LIGHT_VALIDATOR_LOGGER_NAME = 'v_osi.trafficlight.TrafficLightValidator'
TRAFFIC_LIGHT_CLASSIFICATION_VALIDATOR_LOGGER_NAME = 'v_osi.trafficlight.TrafficLightClassificationValidator'

# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

# CONSTANTS
MINIMUM_SURFACE_TEMPERATUE = 0.


class TrafficLightValidator:
    
    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_LIGHT_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data = osi3.osi_trafficlight_pb2.TrafficLight()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug(f'Cheking osi3::TrafficLight object in context "{self.context}"')

        res_a = self._checkID()
        res_b = self._check_base()
        res_c = self._check_classification()
        return res_a and res_b and res_c

    def _checkID(self):        
        """ Check ID recives decoded data """
        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        return id_validator.validate()

    def _check_base(self):
        """ Check the base of traffic sign"""
        base_validator = validation.common.BaseStationaryValidator()
        base_validator.load_data(self._data.base)
        return base_validator.validate()
 
    def _check_classification(self):
        classification_validator = TrafficLightClassificationValidator()
        classification_validator.load_data(self._data.classification)
        return classification_validator.validate()

class TrafficLightClassificationValidator:

    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_LIGHT_CLASSIFICATION_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data   

    def validate(self):
        """ Validate  """

        result = self._check_color()
        
        result_icon = self._check_icon()
        result = result and result_icon

        result_mode = self._check_mode()
        result = result and result_mode
        
        if result_icon == 'ICON_COUNTDOWN_SECONDS' or  result_icon == 'ICON_COUNTDOWN_PERCENT':
            result_counter = self._check_counter()
            result = result and result_counter


        result_lane_id = self._check_assigned_lane_id()
        result = result and result_lane_id

        return result
        
    def _check_color(self):
        """ Checking color of the traffic light """

        # Check if the field is present 
        if not is_set(self._data, 'color'):
            self.log.warning('The field "color" is not present in TrafficLight.Classification')
            return False
        else:
            self.log.debug(f'Field classification.color has value of ({self._data.color})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_trafficlight_pb2.TrafficLight.Classification.Color

        type_name = get_enum_name(enum_wrapper, self._data.color)
        self.log.debug(f'Classification.color name is set to "{type_name}"')
        return str(type_name)  

    def _check_icon(self):
        """ Checking icon of the traffic light """

        # Check if the field is present 
        if not is_set(self._data, 'icon'):
            self.log.warning('The field "icon" is not present in TrafficLight.Classification')
            return False
        else:
            self.log.debug(f'Field classification.icon has value of ({self._data.icon})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_trafficlight_pb2.TrafficLight.Classification.Color

        type_name = get_enum_name(enum_wrapper, self._data.icon)
        self.log.debug(f'Classification.icon name is set to "{type_name}"')
        return str(type_name)  

    def _check_mode(self):
        """ Checking mode of the traffic light """

        # Check if the field is present 
        if not is_set(self._data, 'mode'):
            self.log.warning('The field "mode" is not present in TrafficLight.Classification')
            return False
        else:
            self.log.debug(f'Field classification.mode has value of ({self._data.mode})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_trafficlight_pb2.TrafficLight.Classification.Color

        type_name = get_enum_name(enum_wrapper, self._data.mode)
        self.log.debug(f'Classification.mode name is set to "{type_name}"')
        return str(type_name)

    def _check_counter(self):
        """ Check ice depth of the surface"""
        if not is_set(self._data,'counter'):
            self._log.warning(f'TrafficLight counter is not set')
            return False

        counter = self._data.counter
        self.log.debug('Counter ({}) is valid'.format(counter))
        return True

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
