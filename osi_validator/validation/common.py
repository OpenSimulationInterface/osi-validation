import logging 
import math

import osi3.osi_common_pb2
from validation.osi_utility  import is_set

MODULE_LOGGER_NAME       = 'v_osi.common'
ID_VALIDATOR_LOGGER_NAME = 'v_osi.common.IdentiierValidator'
VECTOR_3D_VALIDATOR_LOGGER_NAME = 'v_osi.common.Vector3dValidator'
VECTOR_2D_VALIDATOR_LOGGER_NAME = 'v_osi.common.Vector2dValidator'
VECTOR_3D_VALIDATOR_LOGGER_NAME = 'v_osi.common.Vector3dValidator'
ORIENTATION_3D_VALIDATOR_LOGGER_NAME = 'v_osi.common.Orientation3dValidator'
DIMENSION_3D_VALIDATOR_LOGGER_NAME = 'v_osi.common.Dimension3dValidator'
BASE_STATIONARY_VALIDATOR_LOGGER_NAME = 'v_osi.common.BaseStationaryValidator'
TIMESTAMP_VALIDATOR_LOGGER_NAME = 'v_osi.common.TimestampValidator'

# Constants
MINIMUM_DIMENSION = 0.0 # meters

# Configure logger for the module
log = logging.getLogger(MODULE_LOGGER_NAME)

class IdentifierValidator:
    IDENTIFIER_MINIMUM_VALUE = 0

    def __init__(self):
        self.log = logging.getLogger(ID_VALIDATOR_LOGGER_NAME)
        self._data = None

    def __repr__(self):
        """String representation """
        return f'Validator for Identifier({self._data.value})'

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Identifier()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """
        
        # Checking if the object is of the Identifier type
        if not isinstance(self._data, osi3.osi_common_pb2.Identifier):
            self.log.warning('Object is not instance of Identifier')
            return False

        # Checkin the value of ID
        value = self._data.value

        if value < self.IDENTIFIER_MINIMUM_VALUE:
            self.log.warning(f'ID {value} outsiede expected range')
            return False 
        else:
            self.log.info(f'ID {value} as expected')
            return True

class Vector3dValidator():

    def __init__(self):
        self.log = logging.getLogger(VECTOR_3D_VALIDATOR_LOGGER_NAME)
        self._data = None

    def __repr__(self):
        """String representation """
        return f'Validator for Vector3d({self._data.x},{self._data.y},{self._data.z})'

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Vector3d()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """
        
        # Checking if the object is of the Identifier type
        if not isinstance(self._data, osi3.osi_common_pb2.Vector3d):
            self.log.warning('Object is not instance of Vector3d')
            return False

        # Checkin the value of ID
        are_Fields_set = True
        if not is_set(self._data,'x'):
            are_Fields_set = False
            self.log.warning('Field x in not set in Vector3d')
        if not is_set(self._data,'y'):
            are_Fields_set = False
            self.log.warning('Field y in not set in Vector3d')
        if not is_set(self._data,'z'):
            are_Fields_set = False
            self.log.warning('Field z in not set in Vector3d')

        if not are_Fields_set:
            return False

        return True

class Vector2dValidator():

    def __init__(self):
        self.log = logging.getLogger(VECTOR_2D_VALIDATOR_LOGGER_NAME)
        self._data = None

    def __repr__(self):
        """String representation """
        return f'Validator for Vector2d({self._data.x},{self._data.y})'

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Vector2d()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """
        
        # Checking if the object is of the Identifier type
        if not isinstance(self._data, osi3.osi_common_pb2.Vector2d):
            self.log.warning('Object is not instance of Vector3d')
            return False

        # Checkin the value of ID
        are_Fields_set = True
        if not is_set(self._data,'x'):
            are_Fields_set = False
            self.log.warning('Field x in not set in Vector2d')
        if not is_set(self._data,'y'):
            are_Fields_set = False
            self.log.warning('Field y in not set in Vector2d')
        
        if not are_Fields_set:
            return False

        self.log.debug(repr(self))
        return True

class Orientation3dValidator():

    def __init__(self):
        self.log = logging.getLogger(ORIENTATION_3D_VALIDATOR_LOGGER_NAME)
        self._data = None
        self.as_angle = None

    def __repr__(self):
        """String representation """
        return f'Validator for Orientation3d({self._data.roll},{self._data.pitch},{self._data.yaw})'

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Orientation3d()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """
        
        # Checking if the object is of the Identifier type
        if not isinstance(self._data, osi3.osi_common_pb2.Orientation3d):
            self.log.warning('Object is not instance of Orientation3d')
            return False

        # Check presence of the fields
        are_Fields_set = True
        if not is_set(self._data,'roll'):
            are_Fields_set = False
            self.log.warning('Field roll in not set in Orientation3d')
        if not is_set(self._data,'pitch'):
            are_Fields_set = False
            self.log.warning('Field pitch in not set in Orientation3d')
        if not is_set(self._data,'yaw'):
            are_Fields_set = False
            self.log.warning('Field yaw in not set in Orientation3d')

        if not are_Fields_set:
            return False

        # Check values sored in the object as they would be an angle.
        # This means additional constrain [-pi,pi)
        if self.as_angle is True:

            are_angles_in_range = True
            # Check pitch
            if not -math.pi < self._data.roll < math.pi:
                self.log.warning('Orientation roll angle ({}) is outside of allowed range.'.format(self._data.pitch))
                are_angles_in_range = False
            
            # Check roll
            if not -math.pi < self._data.pitch < math.pi:
                self.log.warning('Orientation pitch angle ({}) is outside of allowed range.'.format(self._data.pitch))
                are_angles_in_range = False
            
            
            # Check yaw
            if not -math.pi < self._data.yaw < math.pi:
                self.log.warning('Orientation yaw angle ({}) is outside of allowed range.'.format(self._data.yaw))
                are_angles_in_range = False
            
            # return 
            return are_angles_in_range

        return True

class Dimension3dValidator():

    def __init__(self):
        self.log = logging.getLogger(DIMENSION_3D_VALIDATOR_LOGGER_NAME)
        self._data = None

    def __repr__(self):
        """String representation """
        return f'Validator for Dimension3d({self._data.length},{self._data.width},{self._data.height})'

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Dimension3d()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """
        
        # Checking if the object is of the Identifier type
        if not isinstance(self._data, osi3.osi_common_pb2.Dimension3d):
            self.log.warning('Object is not instance of Dimension3d')
            return False

        # Checkin the value of ID
        are_Fields_set = True
        if not is_set(self._data,'length'):
            are_Fields_set = False
            self.log.warning('Field length in not set in Dimension3d')
        if not is_set(self._data,'width'):
            are_Fields_set = False
            self.log.warning('Field width in not set in Dimension3d')
        if not is_set(self._data,'height'):
            are_Fields_set = False
            self.log.warning('Field height in not set in Dimension3d')

        if not are_Fields_set:
            return False

        # Check if values are at least zero
        are_values_correct = True
        if self._data.length < MINIMUM_DIMENSION:
            self.log.warning('Dimension3d.length ({}) is outside allowed range').format(self._data.length)
            are_values_correct = False

        if self._data.width < MINIMUM_DIMENSION:
            self.log.warning('Dimension3d.width ({}) is outside allowed range').format(self._data.width)
            are_values_correct = False


        if self._data.height < MINIMUM_DIMENSION:
            self.log.warning('Dimension3d.height ({}) is outside allowed range').format(self._data.height)
            are_values_correct = False

        return are_values_correct

class BaseStationaryValidator():

    def __init__(self):
        self.log = logging.getLogger(VECTOR_3D_VALIDATOR_LOGGER_NAME)
        self._data = None

    def __repr__(self):
        """String representation """
        return f'Validator for Vector3d({self._data.x},{self._data.y},{self._data.z})'

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Vector3d()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """    

        result_1 = self._check_dimension()
        result_2 = self._check_position()
        result_3 = self._check_orientation()

        return result_1 and result_2 and result_3
        # base_polygon    Vector2d    repeated

    def _check_dimension(self):
        d3dv = Dimension3dValidator()
        d3dv.load_data(self._data.dimension)
        return d3dv.validate()

    def _check_position(self):
        v3dv = Vector3dValidator()
        v3dv.load_data(self._data.position)
        return v3dv.validate()

    def _check_orientation(self):
        o3dv = Orientation3dValidator()
        o3dv.load_data(self._data.orientation)
        o3dv.as_angle = True
        return o3dv.validate()

class TimestampValidator:
    
    MAXIMUM_NANOS_COUNT = 999_999_999

    def __init__(self):
        self.log = logging.getLogger(TIMESTAMP_VALIDATOR_LOGGER_NAME)
        self._data = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_common_pb2.Timestamp()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):   
        if not all([is_set(self._data, 'seconds'),
                    is_set(self._data, 'nanos')]):
                        self.log.warning('Timestamp is not set correctly')
                        return False
        nanos = self._data.nanos
        seconds = self._data.seconds
        
        if nanos > TimestampValidator.MAXIMUM_NANOS_COUNT:
            self.log.warning('Nanoseconds count is abouve the limit {}'.format(nanos))
            return False
        
        if nanos < 0 or seconds < 0 :
            self.log.warning('Timestamp values must be positive integers. Found {}seconds {}nanos'
                            .format(seconds,nanos))
            return False
            

        self.log.info('Timestamp is set to {}s{:09d}ns'.format(seconds,nanos))
        return True


