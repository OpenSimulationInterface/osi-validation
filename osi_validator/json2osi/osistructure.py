#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# Use imports above in anty python2 code

# Python standard library imports
import json

class OsiStructure:
    """ This is utility class for handling information contained in proto definitions of Open Simulation Interface."""
    
    OSI_DEFINITIONS_FILE = 'osi_definitions.json'

    def __init__(self):
        """Initialize Osi Structure with data loaded from the hard drive """
        with open(self.OSI_DEFINITIONS_FILE) as f:
            data = json.load(f)
        self._osi_definitions = data

    def isFieldRepeted(self, object_type, field):
        """Chck if the field is Repeted (iterable)"""
        return self._osi_definitions \
                        [object_type] \
                        ['data_fileds'] \
                        [field] \
                        ['isRepeted']

    def isFieldPrimitive(self, object_type, field):
        """Check if the field in the class is primitive or composite"""
        return self._osi_definitions \
                        [object_type] \
                        ['data_fileds'] \
                        [field] \
                        ['isPrimitive']

    def isClassEnum(self, class_name):
        """ Returns True is the Class is of enumeration Type False otherwise"""
        try:
            return self._osi_definitions[class_name]['isEnum']
        except KeyError:
            return False

    def getFieldType(self,class_name, field):
        """Get type of the osi field as per osi definition
        If can be either composite or primitive type"""
        return self._osi_definitions \
                        [class_name] \
                        ['data_fileds'] \
                        [field] \
                        ['type_name']

    def getFieldClassification(self, object_type, field):
        """Get string classisication of the field"""
        if self.isFieldPrimitive(object_type, field):
            if self.isFieldRepeted(object_type, field):
                return 'PRIMITIVE_ITERABLE'
            else:
                return 'PRIMITIVE_SINGLE'

        if not self.isFieldPrimitive(object_type, field):
            # Additional check if the inner clas is enumeration type
            if self.isClassEnum(self.getFieldType(object_type, field)):
                return 'ENUMERATION'
            if self.isFieldRepeted(object_type, field):
                return 'COMPOSITE_ITERABLE'
            else:
                return 'COMPOSITE_SINGLE'
        return 'NOT_KNOWN'

    def getClassFieldList(self, object_type):
        """Return list of fields defined for a class"""
        return self._osi_definitions[object_type]['data_fileds'].keys()

    def getClassModuleName(self, class_name):
        """Return string of the classes' module"""
        return self._osi_definitions[class_name]['module_name']


if __name__ == "__main__":
    """prevent running as script"""
    print('This file is not stand alone script!')
    raise SystemExit