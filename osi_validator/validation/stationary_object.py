#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import osi3.osi_object_pb2
import copy

class StationaryObjectValidator():

    ID_MINIMUM_VALUE = 1
    BASE_DIMENSIONS_MINIMUM_VALUE = 1
    BASE_BASE_POLYGON_MINIMUM_VERTEX = 3


    OBJECT_NAME = 'StationaryObject'

    def __init__(self):
        self.report = {}

    
    def load_encoded_data(self, encoded_data):
        data = osi3.osi_object_pb2.StationaryObject()
        data.ParseFromString(encoded_data)
        self.load_data(data)

    def load_data(self, data):
        self._data = data

    def validate(self):
        self._checkID()
        self._checkBaseDimensions()
        self._checkBaseOreintation()
        self._checkBasePosition()
        self._checkBaseBasePolygon()
        self._checkType()
        self._checkMaterial()
        self._checkDensity()
        self._checkColor()

    def _checkID(self):
        """This method checks the vlidity of StationaryObject.id
        
        Reqirements:
            * StationaryObject.id is set
            * StationaryObject.id vallue biger then ID_MINIMUM_VALUE (1)

        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        result = {}
        # Check if id is initialized
        if not self._data.HasField('id'):
            print('The message is missing ID in StationaryObject')
            #TODO append to report
            return result

        if self._data.HasField('id'):
            id = copy.copy(self._data.id.value)
            print('ID of the StationaryObject is ', id)

            if id < self.ID_MINIMUM_VALUE:
                print('ID valu outsiede expected range')
                print('ID :', id)
            else:
                print('ID = {} Test passed'.format(id))

    def _checkBaseDimensions(self):
        """Checks the validity of StationaryObject.base.dimension

        Reqirements:
            * StationaryObject.base.dimension.[lengt,hwidth,height] is set
            * StationaryObject.base.dimension.[lengt,hwidth,height] is
                bigger then BASE_DIMENSION_MINIMUM_VALUE

        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if StationaryObject.base is present 
        # Situation "Hopeless" escape
        if not self._data.HasField('base'):
            print('Stationary Object dosn\'t have field base')
            _is_flawless = False
            return

        # Check if StationaryObject.base.dimensions
        if not self._data.base.HasField('dimension'):
            print('StationaryObject.base dosn\'t have field dimension')
            _is_flawless = False
            return

        # Check if fields in StationaryObject.base.dimensions are present
        # length
        if not self._data.base.dimension.HasField('length'):
            print('StationaryObject.base.dimension dosn\'t have field length')
            _is_flawless = False

        
        # width 
        if not self._data.base.dimension.HasField('width'):
            print('StationaryObject.base.dimension dosn\'t have field width')
            _is_flawless = False

        # height
        if not self._data.base.dimension.HasField('height'):
            print('StationaryObject.base.dimension dosn\'t have field height')
            _is_flawless = False


        # Check numerical values
        length = copy.copy(self._data.base.dimension.length)
        width = copy.copy(self._data.base.dimension.length)
        height = copy.copy(self._data.base.dimension.height)

        if length < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('StationaryObject.base.dimension.length smaller than minimum value expected')
            _is_flawless = False

        if width < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('StationaryObject.base.dimension.width smaller than minimum value expected')
            _is_flawless = False

        if height < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('StationaryObject.base.dimension.height smaller than minimum value expected')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('StationaryObject is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with StationaryObject.base.dimension')
            return 

    def _checkBaseOreintation(self):
        """Checks the validity of StationaryObject.base.orientation

        Reqirements:
            * StationaryObject.base.orientation.[roll,pitch,yaw] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if StationaryObject.base is present 
        # Situation "Hopeless" escape
        if not self._data.HasField('base'):
            print('Stationary Object dosn\'t have field base')
            _is_flawless = False
            return

        # Check if StationaryObject.base.dimensions
        if not self._data.base.HasField('orientation'):
            print('StationaryObject.base dosn\'t have field orientation')
            _is_flawless = False
            return

        # Check if fields in StationaryObject.base.dimensions are present
        # length
        if not self._data.base.orientation.HasField('roll'):
            print('StationaryObject.base.orientation dosn\'t have field roll')
            _is_flawless = False

        
        # width 
        if not self._data.base.orientation.HasField('pitch'):
            print('StationaryObject.base.orientation dosn\'t have field pitch')
            _is_flawless = False

        # height
        if not self._data.base.orientation.HasField('yaw'):
            print('StationaryObject.base.orientation dosn\'t have field yaw')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('StationaryObject is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with StationaryObject.base.orientation')
            return 

    def _checkBasePosition(self):
        """Checks the validity of StationaryObject.base.position

        Reqirements:
            * StationaryObject.base.position.[rx,y,z] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if StationaryObject.base is present 
        # Situation "Hopeless" escape
        if not self._data.HasField('base'):
            print('Stationary Object dosn\'t have field base')
            _is_flawless = False
            return

        # Check if StationaryObject.base.dimensions
        if not self._data.base.HasField('position'):
            print('StationaryObject.base dosn\'t have field position')
            _is_flawless = False
            return

        # Check if fields in StationaryObject.base.dimensions are present
        # length
        if not self._data.base.position.HasField('x'):
            print('StationaryObject.base.position dosn\'t have field x')
            _is_flawless = False

        
        # width 
        if not self._data.base.position.HasField('y'):
            print('StationaryObject.base.position dosn\'t have field y')
            _is_flawless = False

        # height
        if not self._data.base.position.HasField('z'):
            print('StationaryObject.base.position dosn\'t have field z')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('StationaryObject.base.position is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with StationaryObject.base.position')
            return 

    def _checkBaseBasePolygon(self):
        """Checks the validity of BaseStationary.base_polygon

        Reqirements:
            * BaseStationary.base_polygon.[repeated_Vector2d] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if BaseStationary.base_polygon is present 
        # Situation "Hopeless" escape
        if len(self._data.base.base_polygon) == self.BASE_BASE_POLYGON_MINIMUM_VERTEX :
            print('BaseStationary dosn\'t have valid field base_polygon')
            _is_flawless = False
            return

        for vertex in self._data.base.base_polygon:
            if not vertex.HasField('x') and not vertex.HasField('y'):
                print('BaseStationary.base_polygon\'s vertex is not valid')
                return

    def _checkType(self):
        """This method checks the vlidity of StationaryObject.type
        
        Reqirements:
            * StationaryObject.type is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.classification.HasField('type'):
            enum_value = self._data.classification.type
            enum_name = self._data.Classification.Color.Name(enum_value)
            print('Found Type', enum_name)
        else:
            print('StationaryObject classification type is not set ')
            return

    def _checkMaterial(self):
        """This method checks the vlidity of StationaryObject.material
        
        Reqirements:
            * StationaryObject.material is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.classification.HasField('material'):
            enum_value = self._data.classification.material
            enum_name = self._data.Classification.Material.Name(enum_value)
            print('Found Material', enum_name)
        else:
            print('StationaryObject classification material is not set ')
               
    def _checkDensity(self):
        """This method checks the vlidity of StationaryObject.density
        
        Reqirements:
            * StationaryObject.density is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.classification.HasField('density'):
            enum_value = self._data.classification.density
            enum_name = self._data.Classification.Density.Name(enum_value)
            print('Found Density', enum_name)
        else:
            print('StationaryObject classification density is not set ')
            
    def _checkColor(self):
        """This method checks the vlidity of StationaryObject.color
        
        Reqirements:
            * StationaryObject.color is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.classification.HasField('color'):
            enum_value = self._data.classification.color
            enum_name = self._data.Classification.Color.Name(enum_value)
            print('Found Color', enum_name)
        else:
            print('StationaryObject classification color is not set ')

