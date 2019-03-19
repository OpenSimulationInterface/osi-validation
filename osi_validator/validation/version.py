import logging 

import osi3.osi_version_pb2
from validation.osi_utility  import is_set

MODULE_LOGGER_NAME       = 'v_osi.version'
VERSION_VALIDATOR_LOGGER_NAME = 'v_osi.version.VersionValidator'

# Configure logger for the module
log = logging.getLogger(MODULE_LOGGER_NAME)

class VersionValidator:
    
    def __init__(self):
        self.log = logging.getLogger(VERSION_VALIDATOR_LOGGER_NAME)
        self._data = None

    def load_data(self, data=None):
        """Load decoded data 
        By decodaed it is understood as already parsed """
        self._data = data
        
    def load_encoded_data(self, encoded_data):
        """ Load protobuf encoded data """
        data =  osi3.osi_version_pb2.InterfaceVersion()
        data.ParseFromString(encoded_data)        
        self.load_data(data)

    def validate(self):
        """ Check validity of class
        - input id must be instance of an Identiier
        - the value must be positive
        """
        if not all([is_set(self._data, 'version_major'),
                   is_set(self._data, 'version_minor'),
                   is_set(self._data, 'version_patch')] ):
                        self.log.warning('Version of the interface is not set')
                        return False

        self.log.info('OSI Version is set to {}.{}.{}'.format(self._data.version_major,
                                                    self._data.version_minor,
                                                    self._data.version_patch))
        return True
