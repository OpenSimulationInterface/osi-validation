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
MODULE_LOGGER_NAME         = 'v_osi.lane'
LANE_VALIDATOR_LOGGER_NAME = 'v_osi.lane.LaneValidator'
ROADCONDITION_VALIDATOR_LOGGER_NAME = 'v_osi.lane.RoadConditionValidator'
LANEPAIR_VALIDATOR_LOGGER_NAME =  'v_osi.lane.LanePairValidator'

LANEBOUNDARY_VALIDATOR_LOGGER_NAME = 'v_osi.lane.LaneBoundaryValidator'
BOUNDARYPOINT_VALIDATOR_LOGGER_NAME = 'v_osi.lane.LaneBoundary.BoundaryPointValidator'
BOUNDARYCLASSIFICATION_VALIDATOR_LOGGER_NAME = 'v_osi.lane.LaneBoundary.ClassificationValidator'

# Configure logger for the module
module_logger = logging.getLogger(MODULE_LOGGER_NAME)

# CONSTANTS
MINIMUM_SURFACE_TEMPERATUE = 0.



class LaneValidator:
    
    def __init__(self):
        self.log = logging.getLogger(LANE_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        if self._data is None:     
            self._data = data
        else:
            self.log.error('Tring to reload data to LaneValidator')

    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_lane_pb2.Lane()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug(f'Cheking osi3::Lane object in context "{self.context}"')

        return self._checkID()

        # Without field classification present further checks are not possible
        if self._check_classification() is True:

            # Check fields within classification
            self._check_is_host_vehicle_lane()
            self._check_centerline_is_driving_direction()
            self._check_road_conditions()
            self._check_lane_pairing()

            lane_type = self._check_classificiation_type()

            # checks only if classification type is 'TYPE_DRIVING'
            if lane_type == 'TYPE_DRIVING':
                self._check_centerline()

            # Perform there checkes only if current lane is not 'TYPE_INTERSECTION'
            if lane_type is not 'TYPE_INTERSECTION':
                self._check_right_adjacent_lane_id()
                self._check_left_adjacent_lane_id()
                self._check_right_lane_boundary_id()
                self._check_left_lane_boundary_id()

            # Perform there checkes only if current lane is of 'TYPE_INTERSECTION'
            if lane_type is  'TYPE_INTERSECTION':
                self._check_free_lane_boundary_id()

    def _check_right_adjacent_lane_id(self):
        """ Check if the field is set and all the values are present"""

        if is_iterable_set(self._data.classification, 'right_adjacent_lane_id') is False:
            self.log.warning(f'Field lane.classification.right_adjacent_lane_id is not set in Lane')
            return False

        ids = self._data.classification.right_adjacent_lane_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid

    def _check_left_adjacent_lane_id(self):
        """ Check if the field is set and all the values are present"""

        if is_iterable_set(self._data.classification, 'left_adjacent_lane_id') is False:
            self.log.warning(f'Field lane.classification.left_adjacent_lane_id is not set in Lane')
            return False

        ids = self._data.classification.left_adjacent_lane_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid

    def _check_right_lane_boundary_id(self):
        """ Check if the field is set and all the values are present"""

        if is_iterable_set(self._data.classification, 'right_lane_boundary_id') is False:
            self.log.warning(f'Field lane.classification.right_lane_boundary_id is not set in Lane')
            return False

        ids = self._data.classification.right_lane_boundary_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid

    def _check_left_lane_boundary_id(self):
        """ Check if the field is set and all the values are present"""

        if is_iterable_set(self._data.classification, 'left_lane_boundary_id') is False:
            self.log.warning(f'Field lane.classification.left_lane_boundary_id is not set in Lane')
            return False

        ids = self._data.classification.left_lane_boundary_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid

    def _check_free_lane_boundary_id(self):
        """ Check if the field is set and all the values are present"""

        if is_iterable_set(self._data.classification, 'free_lane_boundary_id') is False:
            self.log.warning(f'Field lane.classification.free_lane_boundary_id is not set in Lane')
            return False

        ids = self._data.classification.free_lane_boundary_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid

    def _check_lane_pairing(self):
        if is_iterable_set(self._data.classification, 'lane_pairing') is False:
            self.log.warning(f'Field lane.classification.lane_pairing is not set in Lane')
            return False

        pairs = self._data.classification.lane_pairing
        is_every_pair_valid = True

        for pair in pairs:
            pair_validator = LanePairValidator()
            pair_validator.load_data(pair)
            result = pair_validator.validate()
            is_every_pair_valid = is_every_pair_valid and result
        return is_every_pair_valid

    def _checkID(self):        
        """ Check ID recives decoded data """
        if not is_set(self._data.classification, 'road_condition'):
            self.log.warning(f'Field id is not set in Lane')
            return False

        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        id_validator.validate()
        return True

    def _check_classification(self):
        """ Check if field classification is present in Lane object
        If the field is not present return False
        If the field is present return True """
        if not is_set(self._data, 'classification'):
            self.log.warning(f'Field classification is not set in Lane object')
            return False
        else:
            return True

    def _check_classificiation_type(self):
        """ Check for presence of classification.type field 
        If the field is not present return False
        If the field is present return True """
        if not is_set(self._data.classification, 'type'):
            self.log.warning('The field "type" is not present in Lane.classification')
            return False
        else:
            self.log.debug(f'Field classification has valeu of '
                           f'({self._data.classification.type})')

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_lane_pb2.Lane.Classification.Type
        type_name = get_enum_name(enum_wrapper, self._data.classification.type)
        self.log.debug(f'Lane.Classification.type name is set to "{type_name}"')
        return str(type_name)        

    def _check_centerline(self):
        """ Check if centerline is valid """
        cl = self._data.classification.centerline

        is_every_vertex_valid = True

        for index,vertex in enumerate(cl):
            v3D_validator = validation.common.Vector3dValidator()
            v3D_validator.load_data(vertex)
            result = v3D_validator.validate()
            is_every_vertex_valid = is_every_vertex_valid and result

        if is_every_vertex_valid is True:
            self.log.debug('line.classification.centerline is valid.')
            return False

        if is_every_vertex_valid is False:
            self.log.warning('line.classification.centerline is not valid')
            return True

    def _check_is_host_vehicle_lane(self):
        """ Check if field is_host_vehicle_lane is set and valid """
        if not is_set(self._data.classification,'is_host_vehicle_lane'):
            self.log.warning('Field classification.is_host_vehicle is not set in Lane object')
            return False
        self.log.debug(f'Lane.classification.is_host_vehicle_lane field is set'
                       f' to {self._data.classification.is_host_vehicle_lane}')
        return True 

    def _check_road_conditions(self):
        """ Checking RoadConditions validity """
        if not is_set(self._data.classification, 'road_condition'):
            self.log.warning(f'Field road_condition is not set in Lane.classification')
            return False

        rc = RoadConditionValidator()
        rc.load_data(self._data.classification.road_condition)
        rc.validate()
        return True

    def _check_centerline_is_driving_direction(self):
        """ Check if centerline is sorted ascending or descending """
        if not is_set(self._data.classification, 'centerline_is_driving_direction'):
            self.log.warning('Boolean field "centerline_is_driving_direction" has not been set')
            return False
        self.log.debug(f'Field Lane.classification.centerline_is_driving_direction'
            f'is set to {self._data.classification.centerline_is_driving_direction}')
        return True

class RoadConditionValidator:

    def __init__(self):
        self.log = logging.getLogger(ROADCONDITION_VALIDATOR_LOGGER_NAME)
        self._data = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        if self._data is None:     
            self._data = data
        else:
            self.log.error('Tring to reload data to RoadConditions')    

    def validate(self):
        self.log.debug(f'Cheking osi3::Lane::RoadConditions object')

        self._check_surface_temperature()
        self._check_water_film()
        self._check_surface_freezing_point()
        self._check_surface_ice()
        self._check_surface_roughness()
        self._check_surface_texture()

    def _check_surface_temperature(self):
        """Checking if Road Suftace temparature is higher the minimum value """
        if not is_set(self._data,'surface_temperature'):
            self._log.warning(f'Road surface temperature is not set')
            return False

        st = self._data.surface_temperature
        
        if st < MINIMUM_SURFACE_TEMPERATUE:
            self.log.warning(f'Surface temperature ({st} Kelvins) outside permitd range')
            return False
        else:
            self.log.info(f'Surface temperature ({st} Kelvins) is valid')
            return True

    def _check_water_film(self):
        """Checking the depth of water film on the road surface
        The value is in milimiters [mm]
        """
        if not is_set(self._data,'surface_water_film'):
            self._log.warning(f'Road Surface water film is not set')
            return False

        wf = self._data.surface_water_film
        
        if wf < 0:
            self.log.warning(f'Depth of water film on road surface can not be negative')
            return False
        else:
            self.log.info(f'Surface water film ({wf} [mm]) is valid')
            return True 

    def _check_surface_freezing_point(self):
        """ Check freezing point 
        The value is in Kelvins [K]
        """
        if not is_set(self._data,'surface_freezing_point'):
            self._log.warning(f'Road Surface freezing point is not set')
            return False

        fp = self._data.surface_freezing_point
        
        if fp < 0:
            self.log.warning(f'Road Surface freezing point can not be negative')
            return False
        else:
            self.log.info(f'Surface frezzing point ({fp} [K]) is valid')
            return True

    def _check_surface_ice(self):
        """ Check ice depth of the surface"""
        if not is_set(self._data,'surface_ice'):
            self._log.warning(f'Road Surface ice is not set')
            return False

        ice = self._data.surface_ice

        if ice < 0:
            self.log.warning(f'Depth of ice film on road surface can not be negative')
            return False
        else:
            self.log.info(f'Surface ice film ({ice} [mm]) is valid')
            return True

    def _check_surface_roughness(self):
        """ Check ice depth of the surface"""
        if not is_set(self._data,'surface_roughness'):
            self._log.warning(f'Road Surface roughness is not set')
            return False

        roughness = self._data.surface_roughness

        if roughness < 0:
            self.log.warning(f'Road surface roughness can not be negative')
            return False
        else:
            self.log.info(f'Surface roughness ({roughness} [mm/m]) is valid')
            return True

    def _check_surface_texture(self):
        """ Check ice depth of the surface"""
        if not is_set(self._data,'surface_texture'):
            self._log.warning(f'Road Surface texture is not set')
            return False

        texture = self._data.surface_texture

        if texture < 0:
            self.log.warning(f'Road surface texture can not be negative')
            return False
        else:
            self.log.info(f'Surface texture ({texture} [m]) is valid')
            return True

class LanePairValidator:

    def __init__(self):
        self.log = logging.getLogger(LANEPAIR_VALIDATOR_LOGGER_NAME)
        self._data = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        if self._data is None:     
            self._data = data
        else:
            self.log.error('Tring to reload data to LanePair')    

    def validate(self):
        self.log.debug(f'Cheking osi3::Lane.classification.lane_pairing object')

        result_a = self._check_antecessor()
        result_b = self._check_successor()
        return result_a and result_b

    def _check_antecessor(self):
        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.antecessor_lane_id)
        result = id_validator.validate()

    def _check_successor(self):
        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.successor_lane_id)
        result = id_validator.validate()

class LaneBoundaryValidator:
    def __init__(self):
        self.log = logging.getLogger(LANEBOUNDARY_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.context = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        if self._data is None:     
            self._data = data
        else:
            self.log.error('Tring to reload data to LaneBoundaryValidator')

    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_lane_pb2.LaneBoundary()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        self.log.debug(f'Cheking osi3::LaneBoundary object in context "{self.context}"')
        
        result_a = self._check_id()
        result_b = self._check_boundary_line()
        result_c = self._check_classification()

        is_object_valid = result_a and result_b and result_c

        if is_object_valid:
            self.log.info('LaneBoundary object was found to be valid')
        else:
            self.log.warning('LaneBoundary object is not valid')

        return is_object_valid

    def _check_id(self):
        id_validator = validation.common.IdentifierValidator()
        id_validator.load_data(self._data.id)
        result = id_validator.validate()
        return result 

    def _check_boundary_line(self):
        """ Field boundary_line iterable containging BoudaryPoint objects """
        if is_iterable_set(self._data, 'boundary_line') is False:
            self.log.warning(f'Field boundary_line is not set in LaneBoundary')
            return False

        points = self._data.boundary_line
        is_every_point_valid = True

        for point in points:
            bp_validator = BoundaryPointValidator()
            bp_validator.load_data(point)
            result = bp_validator.validate()
            is_every_point_valid = is_every_point_valid and result

        return is_every_point_valid

    def _check_classification(self):
        cl_validator = BoundaryLineClassificationValidator(self._data.classification)
        result = cl_validator.validate()
        return result

class BoundaryPointValidator:

    def __init__(self):
        self.log = logging.getLogger(BOUNDARYPOINT_VALIDATOR_LOGGER_NAME)
        self._data = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        if self._data is None:     
            self._data = data
        else:
            self.log.error('Tring to reload data to BoundaryPoint')    

    def validate(self):
        self.log.debug(f'Cheking osi3.LaneBoundary.BoundaryPoint object')

        result_a = self._check_position()
        result_b = self._check_width()
        result_c = self._check_height()
        
        is_point_valid = result_a and result_b and result_c

        return is_point_valid

    def _check_position(self):
        v3D_validator = validation.common.Vector3dValidator()
        v3D_validator.load_data(self._data.position)
        result = v3D_validator.validate()
        return result

    def _check_width(self):
        is_present = is_set(self._data, 'width')
        if is_present:
            self.log.debug(f'Width of the point is {self._data.width}')
        else:
            self.log.warning(f'Width of the point is not set')
        return is_present

    def _check_height(self):
        is_present = is_set(self._data, 'height')
        if is_present:
            self.log.debug(f'Height of the point is {self._data.height}')
        else:
            self.log.warning(f'Height of the point is not set')
        return is_present
        

class BoundaryLineClassificationValidator:
    def __init__(self, data):
        self.log = logging.getLogger(BOUNDARYCLASSIFICATION_VALIDATOR_LOGGER_NAME)
        self._data = data
    
    def validate(self):
        self.log.debug(f'Cheking osi3.LaneBoundary.BoundaryPoint object')

        result_a = self._check_type()
        result_b = self._check_color()
        result_c = self._check_limiting_structure_id()
        
        is_point_valid = result_a and result_b and result_c

        return is_point_valid

    def _check_type(self):
        """Enum value of type"""

        # Here I need additional information about OSI-protobuf 
        enum_wrapper = osi3.osi_lane_pb2.LaneBoundary.Classification.Type
        type_name = get_enum_name(enum_wrapper, self._data.type)
        self.log.debug(f'LaneBoundry.Classification.type name is set to "{type_name}"')
        if len(type_name):
            return True
        else:
            return False 

    def _check_color(self):
        """ Enum value of color"""
        enum_wrapper = osi3.osi_lane_pb2.LaneBoundary.Classification.Type
        type_name = get_enum_name(enum_wrapper, self._data.color)
        self.log.debug(f'LaneBoundry.Classification.type name is set to "{type_name}"')
        if len(type_name):
            return True
        else:
            return False 

    def _check_limiting_structure_id(self):
        """ Repeated field idicating structure ID"""
        if is_iterable_set(self._data, 'limiting_structure_id') is False:
            self.log.warning(f'Field LaneBoundary.Classification.limiting_structure_id is not set in LaneBoundary')
            return False

        ids = self._data.limiting_structure_id
        is_every_id_valid = True

        for one_id in ids:
            id_validator = validation.common.IdentifierValidator()
            id_validator.load_data(one_id)
            result = id_validator.validate()
            is_every_id_valid = is_every_id_valid and result

        return is_every_id_valid
