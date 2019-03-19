#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging

#Related third party imports.
import osi3.osi_lane_pb2

#Local application specific imports.
import validation.common

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value


# Names of loggers in the module
MODULE_LOGGER_NAME         = 'v_osi.XXXXXX'
YYYYYY_VALIDATOR_LOGGER_NAME = 'v_osi.XXXXXX.YYYYYYYYValidator'

# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

# CONSTANTS
MINIMUM_SURFACE_TEMPERATUE = 0.



class YYYYYYYYValidator:
    
    def __init__(self):
        self.log = logging.getLogger(YYYYYY_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_YYYYY_pb2.Lane()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug('Cheking osi3::YYYYYYYY object in context "{self.context}"')

        self._checkID()

    def _checkID(self):        
        """ Check ID recives decoded data """
        if not is_set(self._data.classification, 'road_condition'):
            self.log.warning('Field id is not set in Lane')
            return False

        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        id_validator.validate()
        return True



# ----------- VALIDATE ENUM -------------------
   def _check_icon(self):
        """ Checking icon of the traffic light """

        # Check if the field is present 
        if not is_set(self._data, 'icon'):
            self.log.warning('The field "icon" is not present in TrafficLight.Classification')
            return False
        else:
            self.log.debug('Field classification.icon has value of ({self._data.icon})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_trafficlight_pb2.TrafficLight.Classification.Color

        type_name = get_enum_name(enum_wrapper, self._data.icon)
        self.log.debug('Classification.icon name is set to "{type_name}"')
        return str(type_name)  


# ---------- VALIDATE PRIMITIVE ---------------- 
 def _check_surface_ice(self):
        """ Check ice depth of the surface"""
        if not is_set(self._data,'surface_ice'):
            self._log.warning('Road Surface ice is not set')
            return False

        ice = self._data.surface_ice

        if ice < 0:
            self.log.warning('Depth of ice film on road surface can not be negative')
            return False
        else:
            self.log.info('Surface ice film ({ice} [mm]) is valid')
            return True

# ----------- Check ID ------------------------
    def _checkID(self):        
        """ Check ID recives decoded data """
        if not is_set(self._data.classification, 'road_condition'):
            self.log.warning('Field id is not set in Lane')
            return False

        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        id_validator.validate()
        return True


# -------- Check repeated ID  ------------------------
def _check_limiting_structure_id(self):
        """ Repeated field idicating structure ID"""
        if is_iterable_set(self._data, 'limiting_structure_id') is False:
            self.log.warning('Field LaneBoundary.Classification.limiting_structure_id is not set in LaneBoundary')
            return False

        ids = self._data.limiting_structure_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid


# --------- Check Classification -----------         
    def _check_classification(self):
        classification_validator = TrafficLightClassificationValidator()
        classification_validator.load_data(self._data.classification)
        return classification_validator.validate()


# ---------- Occupant --------- 
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

# -------- BASE ----------
import validation.common

base_validator = validation.common.BaseStationaryValidator()
base_validator.load_data(self._data.base)
return base_validator.validate()
