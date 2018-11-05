#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import osi3.osi_trafficsign_pb2
import copy

class TrafficSignValidator():

    IDENTIFIER_MINIMUM_VALUE = 0
    BASE_DIMENSIONS_MINIMUM_VALUE = 1
    BASE_BASE_POLYGON_MINIMUM_VERTEX = 3
    
    OBJECT_NAME = 'TrafficSign'

    def __init__(self, encoded_data):

        self.report = {}
        self._data = osi3.osi_trafficsign_pb2.TrafficSign()
        self._data.ParseFromString(encoded_data)
        
        print('Data in the container : \n', self._data)
        print('Data type : ', type(self._data))


    def validate(self):
        self._checkID()
        self._checkMainSignBaseDimensions()
        self._checkMainSignBaseOreintation()
        self._checkMainSignBasePosition()
        self._checkMainSignBaseBasePolygon()
        self._checkMainSignClassificationType()
        self._checkMainSignClassificationDirection()
        self._checkMainSignClassificationVariability()

        """
        self._checkSupplementarySignBaseDimensions()
        self._checkSupplementarySignBaseOreintation()
        self._checkSupplementarySignBasePosition()
        self._checkSupplementarySignBaseBasePolygon()
        """


    def _checkID(self):
        """This method checks the vlidity Identifier
        
        Reqirements:
            * Mainsign.id is set
            * Mainsign.id vallue biger then ID_MINIMUM_VALUE (1)

        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        result = {}
        # Check if id is initialized
        if not self._data.HasField('id'):
            print('The message is missing ID in TrafficSign')
            return result

        if self._data.HasField('id'):
            id = copy.copy(self._data.id.value)
            print('ID of the TrafficSign is ', id)

            if id < self.IDENTIFIER_MINIMUM_VALUE:
                print('ID valu outsiede expected range')
                print('ID :', id)
            else:
                print('ID = {} Test passed'.format(id))

    def _checkMainSignBaseDimensions(self):
        """Checks the validity of MainSign.base.dimension

        Reqirements:
            * MainSign.base.dimension.[lengt,hwidth,height] is set
            * MainSign.base.dimension.[lengt,hwidth,height] is
                bigger then BASE_DIMENSION_MINIMUM_VALUE

        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if MainSign.base is present 
        # Situation "Hopeless" escape
        if not self._data.main_sign.HasField('base'):
            print('Main Sign dosn\'t have field base')
            _is_flawless = False
            return

        # Check if main_sign.base.dimensions
        if not self._data.main_sign.base.HasField('dimension'):
            print('main_sign.base dosn\'t have field dimension')
            _is_flawless = False
            return

        # Check if fields in main_sign.base.dimensions are present
        # length
        if not self._data.main_sign.base.dimension.HasField('length'):
            print('main_sign.base.dimension dosn\'t have field length')
            _is_flawless = False

        
        # width 
        if not self._data.main_sign.base.dimension.HasField('width'):
            print('main_sign.base.dimension dosn\'t have field width')
            _is_flawless = False

        # height
        if not self._data.main_sign.base.dimension.HasField('height'):
            print('main_sign.base.dimension dosn\'t have field height')
            _is_flawless = False


        # Check numerical values
        length = copy.copy(self._data.main_sign.base.dimension.length)
        width = copy.copy(self._data.main_sign.base.dimension.length)
        height = copy.copy(self._data.main_sign.base.dimension.height)

        if length < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('main_sign.base.dimension.length smaller than minimum value expected')
            _is_flawless = False

        if width < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('main_sign.base.dimension.width smaller than minimum value expected')
            _is_flawless = False

        if height < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('main_sign.base.dimension.height smaller than minimum value expected')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('main_sign.base.dimension is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with MainSign.base.dimension')
            return 

    def _checkMainSignBaseOreintation(self):
        """Checks the validity of main_sign.base.orientation

        Reqirements:
            * main_sign.base.orientation.[roll,pitch,yaw] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if main_sign.base is present 
        # Situation "Hopeless" escape
        if not self._data.main_sign.HasField('base'):
            print('Main Sign dosn\'t have field base')
            _is_flawless = False
            return

        # Check if Mainsign.base.dimensions
        if not self._data.main_sign.base.HasField('orientation'):
            print('main_sign.base dosn\'t have field orientation')
            _is_flawless = False
            return

        # Check if fields in main_sign.base.dimensions are present
        # length
        if not self._data.main_sign.base.orientation.HasField('roll'):
            print('main_sign.base.orientation dosn\'t have field roll')
            _is_flawless = False

        
        # width 
        if not self._data.main_sign.base.orientation.HasField('pitch'):
            print('main_sign.base.orientation dosn\'t have field pitch')
            _is_flawless = False

        # height
        if not self._data.main_sign.base.orientation.HasField('yaw'):
            print('main_sign.base.orientation dosn\'t have field yaw')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('main_sign.base.orientation is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with main_sign.base.orientation')
            return 

    def _checkMainSignBasePosition(self):
        """Checks the validity of main_sign.base.position

        Reqirements:
            * main_sign.base.position.[rx,y,z] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if main_sign.base is present 
        # Situation "Hopeless" escape
        if not self._data.main_sign.HasField('base'):
            print('MainSign dosn\'t have field base')
            _is_flawless = False
            return

        # Check if main_sign.base.dimensions
        if not self._data.main_sign.base.HasField('position'):
            print('main_sign.base dosn\'t have field position')
            _is_flawless = False
            return

        # Check if fields in Mainsign.base.dimensions are present
        # length
        if not self._data.main_sign.base.position.HasField('x'):
            print('main_sign.base.position dosn\'t have field x')
            _is_flawless = False

        
        # width 
        if not self._data.main_sign.base.position.HasField('y'):
            print('mains_ign.main_sign.base.position dosn\'t have field y')
            _is_flawless = False

        # height
        if not self._data.main_sign.base.position.HasField('z'):
            print('main_sign.main_sign.base.position dosn\'t have field z')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('mainsign.main_sign.base.position is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with main_sign.base.position')
            return 

    def _checkMainSignBaseBasePolygon(self):
        """Checks the validity of main_sign.base.base_polygon

        Reqirements:
            * BaseStationary.base_polygon.[repeated_Vector2d] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if BaseStationary.base_polygon is  at least three element long
        if len(self._data.main_sign.base.base_polygon) == self.BASE_BASE_POLYGON_MINIMUM_VERTEX :
            print('main_ign.base dosn\'t have valid field base_polygon')
            _is_flawless = False
            return

        for vertex in self._data.main_sign.base.base_polygon:
            if not vertex.HasField('x') and not vertex.HasField('y'):
                print('main_sign.base.base_polygon\'s vertex is not valid')
                return
        print('main_sign.base.base_polygon is checked and valid')

    def _checkMainSignClassificationType(self):
        """This method checks the vlidity of MainSign.Classification.Type
        
        Reqirements:
            * main_sign.classification.type is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.main_sign.classification.HasField('type'):
            enum_value = self._data.main_sign.classification.type
            enum_name = self._data.MainSign.Classification.Type.Name(enum_value)
            print('main_sign type', enum_name)
        else:
            print('mainSign classification type is not set ')
            return

    def _checkMainSignClassificationDirection(self):
        """This method checks the vlidity of MainSign.Classification.Direction
        
        Reqirements:
            * main_sign.classification.direction_scope is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.main_sign.classification.HasField('direction_scope'):
            enum_value = self._data.main_sign.classification.direction_scope
            enum_name = self._data.MainSign.Classification.DirectionScope.Name(enum_value)
            print('main_sign direction_scope', enum_name)
        else:
            print('mainSign classification direction_scope is not set ')
            return

    def _checkMainSignClassificationVariability(self):
        """This method checks the vlidity of MainSign.Classification.Variability
        
        Reqirements:
            * main_sign.classification.variability is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.main_sign.classification.HasField('variability'):
            enum_value = self._data.main_sign.classification.variability
            enum_name = self._data.Variability.Name(enum_value)
            print('main_sign variability', enum_name)
        else:
            print('mainSign classification variability is not set ')
            return

    def _checkSupplementarySignBaseDimensions(self):
        """Checks the validity of SupplementarySign.base.dimension

        Reqirements:
            * SupplementarySign.base.dimension.[lengt,hwidth,height] is set
            * SupplementarySign.base.dimension.[lengt,hwidth,height] is
                bigger then BASE_DIMENSION_MINIMUM_VALUE

        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if SupplementarySign.base is present 
        # Situation "Hopeless" escape
        if not self._data.supplementary_sign.HasField('base'):
            print('Main Sign dosn\'t have field base')
            _is_flawless = False
            return

        # Check if supplementary_sign.base.dimensions
        if not self._data.supplementary_sign.base.HasField('dimension'):
            print('supplementary_sign.base dosn\'t have field dimension')
            _is_flawless = False
            return

        # Check if fields in supplementary_sign.base.dimensions are present
        # length
        if not self._data.supplementary_sign.base.dimension.HasField('length'):
            print('supplementary_sign.base.dimension dosn\'t have field length')
            _is_flawless = False

        
        # width 
        if not self._data.supplementary_sign.base.dimension.HasField('width'):
            print('supplementary_sign.base.dimension dosn\'t have field width')
            _is_flawless = False

        # height
        if not self._data.supplementary_sign.base.dimension.HasField('height'):
            print('supplementary_sign.base.dimension dosn\'t have field height')
            _is_flawless = False


        # Check numerical values
        length = copy.copy(self._data.supplementary_sign.base.dimension.length)
        width = copy.copy(self._data.supplementary_sign.base.dimension.length)
        height = copy.copy(self._data.supplementary_sign.base.dimension.height)

        if length < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('supplementary_sign.base.dimension.length smaller than minimum value expected')
            _is_flawless = False

        if width < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('supplementary_sign.base.dimension.width smaller than minimum value expected')
            _is_flawless = False

        if height < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('supplementary_sign.base.dimension.height smaller than minimum value expected')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('supplementary_sign.base.dimension is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with SupplementarySign.base.dimension')
            return 

    def _checkSupplementarySignBaseOreintation(self):
        """Checks the validity of supplementary_sign.base.orientation

        Reqirements:
            * supplementary_sign.base.orientation.[roll,pitch,yaw] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if supplementary_sign.base is present 
        # Situation "Hopeless" escape
        if not self._data.supplementary_sign.HasField('base'):
            print('Main Sign dosn\'t have field base')
            _is_flawless = False
            return

        # Check if Mainsign.base.dimensions
        if not self._data.supplementary_sign.base.HasField('orientation'):
            print('supplementary_sign.base dosn\'t have field orientation')
            _is_flawless = False
            return

        # Check if fields in supplementary_sign.base.dimensions are present
        # length
        if not self._data.supplementary_sign.base.orientation.HasField('roll'):
            print('supplementary_sign.base.orientation dosn\'t have field roll')
            _is_flawless = False

        
        # width 
        if not self._data.supplementary_sign.base.orientation.HasField('pitch'):
            print('supplementary_sign.base.orientation dosn\'t have field pitch')
            _is_flawless = False

        # height
        if not self._data.supplementary_sign.base.orientation.HasField('yaw'):
            print('supplementary_sign.base.orientation dosn\'t have field yaw')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('supplementary_sign.base.orientation is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with supplementary_sign.base.orientation')
            return 

    def _checkSupplementarySignBasePosition(self):
        """Checks the validity of supplementary_sign.base.position

        Reqirements:
            * supplementary_sign.base.position.[rx,y,z] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if supplementary_sign.base is present 
        # Situation "Hopeless" escape
        if not self._data.supplementary_sign.HasField('base'):
            print('SupplementarySign dosn\'t have field base')
            _is_flawless = False
            return

        # Check if supplementary_sign.base.dimensions
        if not self._data.supplementary_sign.base.HasField('position'):
            print('supplementary_sign.base dosn\'t have field position')
            _is_flawless = False
            return

        # Check if fields in Mainsign.base.dimensions are present
        # length
        if not self._data.supplementary_sign.base.position.HasField('x'):
            print('supplementary_sign.base.position dosn\'t have field x')
            _is_flawless = False

        
        # width 
        if not self._data.supplementary_sign.base.position.HasField('y'):
            print('mains_ign.supplementary_sign.base.position dosn\'t have field y')
            _is_flawless = False

        # height
        if not self._data.supplementary_sign.base.position.HasField('z'):
            print('supplementary_sign.supplementary_sign.base.position dosn\'t have field z')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('mainsign.supplementary_sign.base.position is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with supplementary_sign.base.position')
            return 

    def _checkSupplementarySignBaseBasePolygon(self):
        """Checks the validity of supplementary_sign.base.base_polygon

        Reqirements:
            * BaseStationary.base_polygon.[repeated_Vector2d] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if BaseStationary.base_polygon is  at least three element long
        if len(self._data.supplementary_sign.base.base_polygon) == self.BASE_BASE_POLYGON_MINIMUM_VERTEX :
            print('supplementary_sign.base dosn\'t have valid field base_polygon')
            _is_flawless = False
            return

        for vertex in self._data.supplementary_sign.base.base_polygon:
            if not vertex.HasField('x') and not vertex.HasField('y'):
                print('supplementary_sign.base.base_polygon\'s vertex is not valid')
                return
        print('supplementary_sign.base.base_polygon is checked and valid')

