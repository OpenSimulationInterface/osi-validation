#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging

#Related third party imports.
import osi3.osi_environment_pb2

#Local application specific imports.
import validation.common

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value


# Names of loggers in the module
MODULE_LOGGER_NAME         = 'v_osi.environment'
ENVIROMENT_VALIDATOR_LOGGER_NAME = 'v_osi.environment.EnvironmentalConditionsValidator'

# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

# CONSTANTS
LOWEST_RECORDED_SEA_LEVEL_PRESSURE = 87000 # Lowest see level pressure recorded ever
HIGHEST_RECORDED_SEA_LEVEL_PRESSURE = 110000 # Lowest see level pressure recorded ever

MINIMUM_HUMIDITY = 0
MAXIMUM_HUMIDITY = 100

MINIMUM_TEMPERATURE = 273 - 40 
MAXIMUM_TEMPERATURE = 273 + 70

class EnvironmentalConditionsValidator:     
    def __init__(self):
        self.log = logging.getLogger(ENVIROMENT_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_environment_pb2.EnvironmentalConditions()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug('Cheking osi3::EnvironmentalConditions object in context "{}"'.format(self.context))

        results = []
        results.append(self._check_ambient_illumination())
        results.append(self._check_time_of_day())
        results.append(self._check_atmospheric_pressure())
        results.append(self._check_relative_humidity())
        results.append(self._check_temperature())
        results.append(self._check_precipitation())
        results.append(self._check_fog())

        return all(results)

    def _check_ambient_illumination(self):
        # Check if the field is present 
        if not is_set(self._data, 'ambient_illumination'):
            self.log.warning('The field "ambient_illumination" is not present in EnvironmentalConditions')
            return False
        else:
            self.log.debug('Field ambient_illumination has value of ({})'.format(self._data.ambient_illumination))
        
        enum_wrapper = osi3.osi_environment_pb2.EnvironmentalConditions.AmbientIllumination
        type_name = get_enum_name(enum_wrapper, self._data.ambient_illumination)
        self.log.debug('Field ambient_illumination name is set to "{}"'.format(type_name))

        return True
 
    def _check_precipitation(self):
        # Check if the field is present 
        if not is_set(self._data, 'precipitation'):
            self.log.warning('The field "precipitation" is not present in EnvironmentalConditions')
            return False
        else:
            self.log.debug('Field precipitation has value of ({})'.format(self._data.precipitation))

        enum_wrapper = osi3.osi_environment_pb2.EnvironmentalConditions.Precipitation
        type_name = get_enum_name(enum_wrapper, self._data.precipitation)
        self.log.debug('Field precipitation name is set to "{}"'.format(type_name))
        
        return True

    def _check_fog(self):
        # Check if the field is present 
        if not is_set(self._data, 'fog'):
            self.log.warning('The field "fog" is not present in EnvironmentalConditions')
            return False
        else:
            self.log.debug('Field fog has value of ({})'.format(self._data.fog))

        enum_wrapper = osi3.osi_environment_pb2.EnvironmentalConditions.Fog
        type_name = get_enum_name(enum_wrapper, self._data.fog)
        self.log.debug('Field fog name is set to "{}"'.format(type_name))
        
        return True

    def _check_time_of_day(self):
        # Check if the field is present 
        if not is_set(self._data, 'time_of_day'):
            self.log.warning('The field "time_of_day" is not present in EnvironmentalConditions')
            return False
        else:
            self.log.debug('Field time_of_day has value of ({})'.format(self._data.time_of_day))

     # Check if the inner field is present 
        if not is_set(self._data.time_of_day,'seconds_since_midnight'):
            self.log.warning('The field "seconds_since_midnight:" is not present in TimeOfDay')
            return False
        else:
            self.log.debug('Field TimeOfDay.seconds_since_midnight: has value of ({})'
                .format(self._data.time_of_day.seconds_since_midnight))
        return True

    def _check_atmospheric_pressure(self):
        """ Check atmospheric_pressure """
        if not is_set(self._data,'atmospheric_pressure'):
            self.log.warning('The field "atmospheric_pressure" is not present in EnvironmentalCondition')
            return False

        p = self._data.atmospheric_pressure

        if p < LOWEST_RECORDED_SEA_LEVEL_PRESSURE:
            self.log.warning('The atmospheric_pressure in EnvironmentalConditions is very low = ({})'.format(p))
            return False
        if p > HIGHEST_RECORDED_SEA_LEVEL_PRESSURE:
            self.log.warning('The atmospheric_pressure in EnvironmentalConditions is very high = ({})'.format(p))
            return False
        else:
            self.log.debug('The atmospheric_pressure in EnvironmentalConditions is = ({})'.format(p))
            return True

    def _check_relative_humidity(self):
        """ Check humidity """
        if not is_set(self._data,'relative_humidity'):
            self.log.warning('The field "relative_humidity" is not present in EnvironmentalCondition')
            return False

        humidity = self._data.relative_humidity

        if humidity < MINIMUM_HUMIDITY:
            self.log.warning('The humidity in EnvironmentalConditions is very low = ({})'.format(humidity))
            return False
        if humidity > MAXIMUM_HUMIDITY:
            self.log.warning('The humidity in EnvironmentalConditions is very high = ({})'.format(humidity))
            return False
        else:
            self.log.debug('The humidity in EnvironmentalConditions is = ({})'.format(humidity))
            return True

    def _check_temperature(self):
        """ Check temperature """
        if not is_set(self._data,'temperature'):
            self.log.warning('The field "temperature" is not present in EnvironmentalCondition')
            return False

        temperature = self._data.temperature

        if temperature < MINIMUM_TEMPERATURE:
            self.log.warning('The temperature in EnvironmentalConditions is very low = ({})K'.format(temperature))
            return False
        if temperature > MAXIMUM_TEMPERATURE:
            self.log.warning('The temperature in EnvironmentalConditions is very high = ({})K'.format(temperature))
            return False
        else:
            self.log.debug('The temperature in EnvironmentalConditions is = ({})K'.format(temperature))
            return True
