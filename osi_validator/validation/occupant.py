#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging

#Related third party imports.
import osi3.osi_occupant_pb2

#Local application specific imports.
import validation.common

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value

# Names of loggers in the module
MODULE_LOGGER_NAME         = 'v_osi.occupant'
OCCUPANT_VALIDATOR_LOGGER_NAME = 'v_osi.occupant.OccupantValidator'
OCCUPANT_CLASSIFICATION_VALIDATOR_LOGGER_NAME= 'v_osi.occupant.OccupantClassificationValidator'
# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

# CONSTANTS
MINIMUM_SURFACE_TEMPERATUE = 0.



class OccupantValidator:
    
    def __init__(self):
        self.log = logging.getLogger(OCCUPANT_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_occupant_pb2.Occupant()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug(f'Cheking osi3::Occupant object in context "{self.context}"')

        result_a = self._checkID()
        result_b = self._check_classification()

        return result_a and result_b

    def _checkID(self):        
        """ Check ID recives decoded data """
        if not is_set(self._data, 'id'):
            self.log.warning(f'Field id is not set in Lane')
            return False

        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        id_validator.validate()
        return True

    def _check_classification(self):
        classification_validator = OccupantClassificationValidator()
        classification_validator.load_data(self._data.classification)
        return classification_validator.validate()

class OccupantClassificationValidator:

    def __init__(self):
        self.log = logging.getLogger(OCCUPANT_CLASSIFICATION_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data   

    def validate(self):
        result_a = self._check_is_driver()
        result_b = self._check_seat()
        result_c = self._check_steering_control()
        
    def _check_is_driver(self):
        """ Check ice depth of the surface"""
        if not is_set(self._data,'is_driver'):
            self.log.warning('Occupant "is_driver" flag is not set')
            return False
        else:
            self.log.debug('Occupant "is_driver" flag is set to "{}"'.format(self._data.is_driver))
            return True

    def _check_seat(self):
        if not is_set(self._data, 'seat'):
            self.log.warning('The field "seat" is not present in Occupant.Classification')
            return False
        else:
            self.log.debug(f'Field classification.seat has value of ({self._data.seat})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_occupant_pb2.Occupant.Classification.Seat

        enum_name = get_enum_name(enum_wrapper, self._data.seat)
        self.log.debug('Occupant.Classification.seat name is set to "{}"'.format({enum_name}))
        return str(enum_name) 


    def _check_steering_control(self):
        if not is_set(self._data, 'steering_control'):
            self.log.warning('The field "steering_control" is not present in Occupant.Classification')
            return False
        else:
            self.log.debug(f'Field classification.steering_control has value of ({self._data.steering_control})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_occupant_pb2.Occupant.Classification.SteeringControl

        enum_name = get_enum_name(enum_wrapper, self._data.steering_control)
        self.log.debug('Occupant.Classification.steering_control name is set to "{}"'.format(enum_name))
        return str(enum_name) 
