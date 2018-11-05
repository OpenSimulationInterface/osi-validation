#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import osi3.osi_object_pb2
import copy

class MovingObjectVaidator():

    ID_MINIMUM_VALUE = 1
    BASE_DIMENSIONS_MINIMUM_VALUE = 1
    BASE_BASE_POLYGON_MINIMUM_VERTEX = 3

    OBJECT_NAME = 'MovigObject'

    def __init__(self):

        self.report = {}
    
    def load_encoded_data(self,encoded_data):
        data = osi3.osi_object_pb2.MovingObject()
        data.ParseFromString(encoded_data)


    def load_data(self,data):
        self._data = data

    def validate(self):
        self._checkID()
        self._checkBaseDimensions()
        self._checkBaseOreintation()
        self._checkBasePosition()
        self._checkBaseBasePolygon()
        self._checkVechicleAttributesDriverId()
        self._checkVechicleAttributesNumberWheels()
        self._checkVehicleClassificationType()
        self._checkVehicleClassificationHasTrailer()
        self._checkVechicleAttributesGroundClearance()

    def _checkID(self):
        """This method checks the vlidity of MovingObject.id
        
        Reqirements:
            * MovingObject.id is set
            * MovingObject.id vallue biger then ID_MINIMUM_VALUE (1)

        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        result = {}
        # Check if id is initialized
        if not self._data.HasField('id'):
            print('The message is missing ID in MovingObject')
            #TODO append to report
            return result

        if self._data.HasField('id'):
            id = copy.copy(self._data.id.value)
            print('ID of the MovingObject is ', id)

            if id < self.ID_MINIMUM_VALUE:
                print('ID valu outsiede expected range')
                print('ID :', id)
            else:
                print('ID = {} Test passed'.format(id))

    def _checkBaseDimensions(self):
        """Checks the validity of MovingObject.base.dimension

        Reqirements:
            * MovingObject.base.dimension.[lengt,hwidth,height] is set
            * MovingObject.base.dimension.[lengt,hwidth,height] is
                bigger then BASE_DIMENSION_MINIMUM_VALUE

        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if MovingObject.base is present 
        # Situation "Hopeless" escape
        if not self._data.HasField('base'):
            print('Moving Object dosn\'t have field base')
            _is_flawless = False
            return

        # Check if MovingObject.base.dimensions
        if not self._data.base.HasField('dimension'):
            print('MovingObject.base dosn\'t have field dimension')
            _is_flawless = False
            return

        # Check if fields in MovingObject.base.dimensions are present
        # length
        if not self._data.base.dimension.HasField('length'):
            print('MovingObject.base.dimension dosn\'t have field length')
            _is_flawless = False

        
        # width 
        if not self._data.base.dimension.HasField('width'):
            print('MovingObject.base.dimension dosn\'t have field width')
            _is_flawless = False

        # height
        if not self._data.base.dimension.HasField('height'):
            print('MovingObject.base.dimension dosn\'t have field height')
            _is_flawless = False


        # Check numerical values
        length = copy.copy(self._data.base.dimension.length)
        width = copy.copy(self._data.base.dimension.length)
        height = copy.copy(self._data.base.dimension.height)

        if length < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('MovingObject.base.dimension.length smaller than minimum value expected')
            _is_flawless = False

        if width < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('MovingObject.base.dimension.width smaller than minimum value expected')
            _is_flawless = False

        if height < self.BASE_DIMENSIONS_MINIMUM_VALUE:
            print('MovingObject.base.dimension.height smaller than minimum value expected')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('MovingObject is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with MovingObject.base.dimension')
            return 

    def _checkBaseOreintation(self):
        """Checks the validity of MovingObject.base.orientation

        Reqirements:
            * MovingObject.base.orientation.[roll,pitch,yaw] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if MovingObject.base is present 
        # Situation "Hopeless" escape
        if not self._data.HasField('base'):
            print('Moving Object dosn\'t have field base')
            _is_flawless = False
            return

        # Check if MovingObject.base.dimensions
        if not self._data.base.HasField('orientation'):
            print('MovingObject.base dosn\'t have field orientation')
            _is_flawless = False
            return

        # Check if fields in MovingObject.base.dimensions are present
        # length
        if not self._data.base.orientation.HasField('roll'):
            print('MovingObject.base.orientation dosn\'t have field roll')
            _is_flawless = False

        
        # width 
        if not self._data.base.orientation.HasField('pitch'):
            print('MovingObject.base.orientation dosn\'t have field pitch')
            _is_flawless = False

        # height
        if not self._data.base.orientation.HasField('yaw'):
            print('MovingObject.base.orientation dosn\'t have field yaw')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('MovingObject is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with MovingObject.base.orientation')
            return 

    def _checkBasePosition(self):
        """Checks the validity of MovingObject.base.position

        Reqirements:
            * MovingObject.base.position.[rx,y,z] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """

        _is_flawless = True

        # Check if MovingObject.base is present 
        # Situation "Hopeless" escape
        if not self._data.HasField('base'):
            print('Moving Object dosn\'t have field base')
            _is_flawless = False
            return

        # Check if MovingObject.base.dimensions
        if not self._data.base.HasField('position'):
            print('MovingObject.base dosn\'t have field position')
            _is_flawless = False
            return

        # Check if fields in MovingObject.base.dimensions are present
        # length
        if not self._data.base.position.HasField('x'):
            print('MovingObject.base.position dosn\'t have field x')
            _is_flawless = False

        
        # width 
        if not self._data.base.position.HasField('y'):
            print('MovingObject.base.position dosn\'t have field y')
            _is_flawless = False

        # height
        if not self._data.base.position.HasField('z'):
            print('MovingObject.base.position dosn\'t have field z')
            _is_flawless = False

        # If all test were pased return some information
        if _is_flawless:
            print('MovingObject.base.position is checked and correct')
            return 

        if not _is_flawless:
            print('Problems detected with MovingObject.base.position')
            return 

    def _checkBaseBasePolygon(self):
        """Checks the validity of MovingObject.base.base_polygon

        Reqirements:
            * MovingObject.base.base_polygon.[repeated_Vector2d] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """
        _is_flawless = True

        # Check if Base.base_polygon is present 
        # Situation "Hopeless" escape
        if len(self._data.base.base_polygon) == self.BASE_BASE_POLYGON_MINIMUM_VERTEX :
            print('Base  dosn\'t have valid field base_polygon')
            _is_flawless = False
            return

        for vertex in self._data.base.base_polygon:
            if not vertex.HasField('x') and not vertex.HasField('y'):
                print('Base.base_polygon\'s vertex is not valid')
                retur

    def _checkVehicleClassificationType(self):
        """This method checks the vlidity of MainSign.Classification.Type
        
        Reqirements:
            * main_sign.classification.type is set
            
        Side effects:
            * method writes to self.report

        Returns:
            * structure written to the report
        """
        if self._data.HasField('vehicle_classification'):
            enum_value = self._data.vehicle_classification.type
            enum_name = self._data.VehicleClassification.Type.Name(enum_value)
            print('Vahicle clasification type', enum_name)
        else:
            print('Vehicle classification type is not set ')
            return

    def _checkVehicleClassificationHasTrailer(self):
        """Checks the validity of MovingObject.vehicle_classification.has_trailer

        Reqirements:
            * vehicle_classification.has_trailer is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report
        """
        _is_flawless = True

        # Check if Base.base_polygon is present 
        # Situation "Hopeless" escape
        if not self._data.vehicle_classification.HasField('has_trailer'):
            print('Moving Object dosn\'t have field has_trailer')
            _is_flawless = False
            return
        else:
            print('MovingObject.vehicle_classification.has_trailer checked')


    def _checkVechicleAttributesDriverId(self):
        """Checks the validity of MovingObject.base.base_polygon

        Reqirements:
            * MovingObject.base.base_polygon.[repeated_Vector2d] is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report

        """
        _is_flawless = True

        # Check if Base.base_polygon is present 
        # Situation "Hopeless" escape
        if not self._data.vehicle_attributes.HasField('driver_id'):
            print('Moving Object dosn\'t have field driver_id')
            _is_flawless = False
            return
        else:
            print('MovingObject.vehicle_attributes.driver_id checked')

    def _checkVechicleAttributesNumberWheels(self):
        """Checks the validity of MovingObject.vehicle_attributes.number_wheels 

        Reqirements:
            * MovingObjectvehicle_attributes.number_wheels  is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report

        """
        _is_flawless = True

        # Check if Base.base_polygon is present 
        # Situation "Hopeless" escape
        if not self._data.vehicle_attributes.HasField('number_wheels'):
            print('Moving Object dosn\'t have field number_wheels')
            _is_flawless = False
            return
        else:
            print('MovingObject.vehicle_attributes.number_wheels checked')

    def _checkVechicleAttributesGroundClearance(self):
        """Checks the validity of MovingObject.vehicle_attributes.ground_clearance 

        Reqirements:
            * MovingObjectvehicle_attributes.ground_clearance  is set
    
        Side effects:
            * write to self.report

        Returns:
            * structure written to the report

        """
        _is_flawless = True

        # Check if Base.base_polygon is present 
        # Situation "Hopeless" escape
        if not self._data.vehicle_attributes.HasField('ground_clearance'):
            print('Moving Object dosn\'t have field ground_clearance')
            _is_flawless = False
            return
        else:
            print('MovingObject.vehicle_attributes.ground_clearance checked')

