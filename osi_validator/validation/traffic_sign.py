#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging

#Related third party imports.
import osi3.osi_trafficsign_pb2

#Local application specific imports.
import validation.common

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value


# Names of loggers in the module
MODULE_LOGGER_NAME = 'v_osi.trafficsign'
TRAFFIC_SIGN_VALUE_VALIDATOR_LOGGER_NAME = \
'v_osi.trafficsign.TrafficSignValueValidator'
TRAFFIC_SIGN_VALIDATOR_LOGGER_NAME = \
'v_osi.trafficsign.TrafficSignValidator'
TRAFFIC_SIGN_MAIN_VALIDATOR_LOGGER_NAME = \
'v_osi.trafficsign.TrafficSignMainValidator'
TRAFFIC_SIGN_MAIN_CLASSIFICATION_VALIDATOR_LOGGER_NAME =\
'v_osi.trafficsign.TrafficSignMainClassificationValidator'
TRAFFIC_SIGN_SUPPLEMENTARY_VALIDATOR_LOGGER_NAME = \
'v_osi.trafficsign.TrafficSignSupplementaryValidator'
TRAFFIC_SIGN_VARIABILITY_VALIDATOR_LOGGER_NAME = \
'v_osi.trafficsign.TrafficSignVariabilityValidator'


# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

class TrafficSignValueValidator:
    
    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_SIGN_VALUE_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def validate(self):
        self.log.debug('Cheking osi3::TrafficSignValue object in context "{}"'.format(self.context))

        result_a = self._check_value()
        result_b = self._check_unit()
        return result_a and result_b

    def _check_value(self):
        if not is_set(self._data,'value'):
            self._log.warning('TrafficSignValue "value" is not set')
            return False
        else:
            self._log.debug('TrafficSignValue "value" is {}'.format(self._data.value))
            return True


    def _check_unit(self):

        # Check if the field is present 
        if not is_set(self._data, 'value_unit'):
            self.log.warning('The field "value_unit" is not present in TrafficSignValue')
            return False
        else:
            self.log.debug('Field classification.icon has value of ({})'.format(self._data.TrafficSignValue))

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_trafficsign_pb2.TrafficSignValue.Unit

        enum_name = get_enum_name(enum_wrapper, self._data.icon)
        self.log.debug('TrafficSignValue name is set to "{}"'.format(enum_name))
        return str(en_name)  

class TrafficSignValidator:
    
    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_SIGN_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_trafficsign_pb2.TrafficSign()

        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug('Cheking osi3::TrafficSign object in context "{}"'.format(self.context))

        result = True
        result_a = self._checkID()
        result_b = self._check_main_sign()
        result_c = self._check_supplementary_sign()

        return result_a and result_b and result_c

    def _checkID(self):        
        """ Check ID recives decoded data """
        if not is_set(self._data, 'id'):
            self.log.warning('Field "id" is not set in TrafficSign')
            return False

        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        id_validator.validate()
        return True

    def _check_main_sign(self):
        if not is_set(self._data, 'main_sign'):
            self.log.warning('Field "main_sign" is not set in TrafficSign')
            return False

        main_sign_validator = TrafficSignMainValidator()
        main_sign_validator.load_data(self._data.main_sign)
        return main_sign_validator.validate()
    
    def _check_supplementary_sign(self):
        if not is_iterable_set(self._data, 'supplementary_sign'):
            self.log.warning('Field "supplementary_sign" is not set in TrafficSign')
            return False

        is_every_sign_valid = True

        for sign in self._data.supplementary_sign:
            supplementary_sign_validator = TrafficSignSupplementaryValidator()
            supplementary_sign_validator.load_data(sign)
            result = supplementary_sign_validator.validate()
            is_every_sign_valid = is_every_sign_valid and result
        return is_every_sign_valid

class TrafficSignMainValidator:
    
    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_SIGN_MAIN_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data

    def validate(self):
        self.log.debug('Cheking osi3::TrafficSign object in context "{}"'.format(self.context))

        result_a = self._check_base()
        result_b = self._check_classification()
        return result_a and result_b

    def _check_base(self):
        if not is_set(self._data, 'base'):
            self.log.warning('Field "base" is not set in TrafficSignMain')
            return False

        base_validator = validation.common.BaseStationaryValidator()
        base_validator.load_data(self._data.base)
        return base_validator.validate()


    def _check_classification(self):
        if not is_set(self._data, 'classification'):
            self.log.warning('Field "classification" is not set in TrafficSignMain')
            return False

        classification_validator = TrafficSignMainClassificationValidator()
        classification_validator.load_data(self._data.classification)
        return classification_validator.validate()


class TrafficSignMainClassificationValidator:

    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_SIGN_MAIN_CLASSIFICATION_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        self._data = data   

    def validate(self):
        is_valid = True
        is_valid = is_valid and self._check_variability()
        is_valid = is_valid and self._check_type()
        is_valid = is_valid and self._check_value()
        is_valid = is_valid and self._check_direction_scope()
        is_valid = is_valid and self._check_assigned_lane_id()
        return is_valid

    def _check_variability(self):
        pass
    #     if not is_set(self._data, 'variability'):
    #         self.log.warning('The field "variability" is not present in TrafficSign.Main.Classification:')
    #         return False
    #     else:
    #         self.log.debug('The field "variability" is set to "{}"'\
    #             .format(self._data.variability))

    #     self.log.warning('The field "icon" is not present in TrafficLight.Classification')
    #         return False
    #     else:
    #         self.log.debug('Field classification.icon has value of ({self._data.icon})')

    #     # Here I need additional information about OSI-protobuf 
    #     enum_wrapper = osi3.osi_trafficsign_pb2.TrafficSign.Variability

    #     type_name = get_enum_name(enum_wrapper, self._data.icon)
    #     self.log.debug('Classification.icon name is set to "{type_name}"')
    #     return str(type_name)  


    def _check_type(self):
        pass
    def _check_value(self):
        pass
    def _check_direction_scope(self):
        pass
    def _check_assigned_lane_id(self):
        pass

# variability     TrafficSign::Variability  
# type            TrafficSign::MainSign::Classification::Type
# value           TrafficSignValue  
# direction_scope TrafficSign::MainSign::Classification::DirectionScope 
# assigned_lane_id Identifier  repeated







# ==========================================================

class TrafficSignSupplementaryValidator:
    
    def __init__(self):
        self.log = logging.getLogger(TRAFFIC_SIGN_VARIABILITY_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data

    def validate(self):
        self.log.debug('Cheking osi3::TrafficSign object in context "{}"'.format(self.context))

        result = True
        result_a = self._checkID()

        return result 

    def _checkID(self):   
        pass 
