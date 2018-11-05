#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports.
import logging

#Related third party imports.
import osi3.osi_lane_pb2

#Local application specific imports.
import validation.common

from validation.version import VersionValidator
from validation.environment import EnvironmentalConditionsValidator
from validation.stationary_object import StationaryObjectValidator
from validation.moving_object import MovingObjectVaidator
from validation.traffic_sign import TrafficSignValidator
from validation.traffic_light import TrafficLightValidator
from validation.occupant import OccupantValidator
from validation.road_marking import RoadMarkingValidator
from validation.environment import EnvironmentalConditionsValidator
import validation.lane as lane

from validation.osi_utility import is_set
from validation.osi_utility import is_iterable_set
from validation.osi_utility import get_enum_name
from validation.osi_utility import get_enum_value


# Names of loggers in the module
MODULE_LOGGER_NAME         = 'v_osi.ground_truth'
GROUND_TRUTH_VALIDATOR_LOGGER_NAME = 'v_osi.ground_truth.GroundTruth.Validator'

# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

# CONSTANTS
MINIMUM_SURFACE_TEMPERATUE = 0.



class GroundTruthValidator:
    
    def __init__(self):
        self.log = logging.getLogger(GROUND_TRUTH_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
       
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_groundtruth_pb2.Lane()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug('Cheking osi3::GroundTruth object.')

        results = []

        iv_result = self._check_InterfaceVersion()
        results.append(iv_result)

        timestamp_result = self._check_Timestamp()
        results.append(timestamp_result)

        host_v_id_result = self._check_host_vahicle_id()
        results.append(host_v_id_result)

        country_code_results = self._check_country_code()
        results.append(country_code_results)

        ec_result = self._checkEnvironmentalConditions()
        results.append(ec_result)

        so_result = self._check_multiple_StationaryObject()
        results.append(so_result)

        mo_result = self._check_multiple_MovingObject()
        results.append(mo_result)

        ts_result = self._check_multiple_TrafficSign()
        results.append(ts_result)

        tl_result = self._check_multiple_TrafficLight()
        results.append(tl_result)

        rm_result = self._check_multiple_RoadMarking()
        results.append(rm_result)

        lb_result = self._check_multiple_LaneBoundary()
        results.append(lb_result)

        l_result = self._check_multiple_Lane()
        results.append(l_result)

        o_result = self._check_multiple_Occupant()
        results.append(o_result)


        return all(results)

    def _checkEnvironmentalConditions(self):
        environmental_conditions_validator = EnvironmentalConditionsValidator()
        environmental_conditions_validator.load_data(self._data.environmental_conditions)
        environmental_conditions_validator.context = 'Ground Truth'
        return environmental_conditions_validator.validate()

    def _check_multiple_StationaryObject(self):
        if is_iterable_set(self._data, 'stationary_object') is False:
            self.log.warning('Field stationary_object is not set in Ground Truth')
            return False

        objects = self._data.stationary_object
        results = []

        for object in objects:
            so_validator = StationaryObjectValidator()
            so_validator.load_data(object)
            result = so_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_MovingObject(self):
        if is_iterable_set(self._data, 'moving_object') is False:
            self.log.warning('Field moving_object is not set in Ground Truth')
            return False

        objects = self._data.moving_object
        results = []

        for object in objects:
            mo_validator = MovingObjectVaidator()
            mo_validator.load_data(object)
            result = mo_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_TrafficSign(self):
        if is_iterable_set(self._data, 'traffic_sign') is False:
            self.log.warning('Field "traffic_sign" is not set in Ground Truth')
            return False

        objects = self._data.traffic_sign
        results = []

        for object in objects:
            ts_validator = TrafficSignValidator()
            ts_validator.load_data(object)
            result = ts_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_TrafficLight(self):

        if is_iterable_set(self._data, 'traffic_light') is False:
            self.log.warning('Field "traffic_light" is not set in Ground Truth')
            return False

        objects = self._data.traffic_light
        results = []

        for object in objects:
            tl_validator = TrafficLightValidator()
            tl_validator.load_data(object)
            result = tl_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_RoadMarking(self):
        
        if is_iterable_set(self._data, 'road_marking') is False:
            self.log.warning('Field "road_marking" is not set in Ground Truth')
            return False

        objects = self._data.road_marking
        results = []

        for object in objects:
            rm_validator = RoadMarkingValidator()
            rm_validator.load_data(object)
            result = rm_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_LaneBoundary(self):
        
        if is_iterable_set(self._data, 'lane_boundary') is False:
            self.log.warning('Field "lane_boundary" is not set in Ground Truth')
            return False

        objects = self._data.lane_boundary
        results = []

        for object in objects:
            lb_validator = lane.LaneBoundaryValidator()
            lb_validator.load_data(object)
            result = lb_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_Lane(self):
        
        if is_iterable_set(self._data, 'lane') is False:
            self.log.warning('Field "lane" is not set in Ground Truth')
            return False

        objects = self._data.lane
        results = []

        for object in objects:
            l_validator = lane.LaneValidator()
            l_validator.load_data(object)
            result = l_validator.validate()
            results.append(result)

        return all(results)

    def _check_multiple_Occupant(self):
        
        if is_iterable_set(self._data, 'occupant') is False:
            self.log.warning('Field "occupant" is not set in Ground Truth')
            return False

        objects = self._data.occupant
        results = []

        for object in objects:
            o_validator = OccupantValidator()
            o_validator.load_data(object)
            result = o_validator.validate()
            results.append(result)

        return all(results)

    def _check_InterfaceVersion(self):
        """ Check Interfae Version """
        if not is_set(self._data, 'version'):
            self.log.warning('Field "version" is not set in GrundTruth')
            return False
        id_validator = VersionValidator()
        id_validator.load_data(self._data.version)
        return id_validator.validate()        
    
    def _check_Timestamp(self):
        """ Check Timestamp """
        if not is_set(self._data, 'timestamp'):
            self.log.warning('Field "timestamp" is not set in GrundTruth')
            return False
        id_validator = validation.common.TimestampValidator()
        id_validator.load_data(self._data.timestamp)
        return id_validator.validate()

    def _check_host_vahicle_id(self):
        """ Check Host vehicle ID """
        if not is_set(self._data, 'host_vehicle_id'):
            self.log.warning('Field "host_vehicle_id" is not set in GrundTruth')
            return False
        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.host_vehicle_id)
        return id_validator.validate()
        
    def _check_country_code(self):
        if not is_set(self._data, 'country_code'):
            self.log.warning('Field "country_code" is not set in GrundTruth')
            return False
        self.log.info('Country code is set to {}'.format(self._data.country_code))
        return False
