#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Python standard library imports
import json
import operator
import importlib
import argparse

# Third party imports
# none

# Local application specifis imports
from osistructure import OsiStructure


class OsiJsonCreator:
    """This class enable cration of osi data structure """
    
    def __init__(self, osi_structure, object_type):
        """ Initalize the object with definitions of osi data str """
        self._osi = osi_structure
        self._object_type = object_type
        
        module_name = self._osi.getClassModuleName(object_type)
        self._osi_object = self.getInstance(module_name, object_type)

    def getInstance(self, module_name, class_name):
        """ Load instance of the class from specified module """

        # Find and load module
        print('Loading Class "{}" from "{}" module_name'
                .format(class_name, module_name))
        module = importlib.import_module(module_name)
        return operator.attrgetter(class_name)(module)()

        
    def buildFromJSON(self, data):
        """ Recursivley build osi data structure based on inlut JSON """
        for field in data.keys():
            # Check if data field is present in object definition
            if field not in self._osi.getClassFieldList(self._object_type):
                print('Field "{}" not present in object "{}"'
                    .format(field, self._object_type))
                continue
            else:
                field_classification = self._osi.getFieldClassification(
                    self._object_type, field)
                field_data = data[field]

                if field_classification == 'COMPOSITE_SINGLE':
                    self.setCompositeSingle(field, field_data)

                if field_classification == 'COMPOSITE_ITERABLE':
                    self.setCompositeRepeated(field, field_data)                   
                if field_classification == 'PRIMITIVE_SINGLE':

                    self.setPrimitiveSingle(field, field_data)

                if field_classification == 'ENUMERATION':
                    self.setEnumeration(field, field_data)

    def setCompositeSingle(self, field, field_data):
        field_type = self._osi.getFieldType(self._object_type, field)

        inner_creator = OsiJsonCreator(self._osi, field_type)
        inner_creator.buildFromJSON(field_data)

        # Setting the data
        field_reference = getattr(self._osi_object, field)
        field_reference.MergeFrom(inner_creator.getOsi())

    def setCompositeRepeated(self, field, field_data):
        print('Processing composite repeted field')

        field_type = self._osi.getFieldType(self._object_type, field)
        field_reference = getattr(self._osi_object, field)

        for element in field_data:
            print(element)
            inner_creator = OsiJsonCreator(self._osi, field_type)
            inner_creator.buildFromJSON(element)
            element_reference = field_reference.add()
            element_reference.MergeFrom(inner_creator.getOsi())        

    def setPrimitiveSingle(self, field, field_data):
        print('Processing primitive field')

        setattr(self._osi_object, field, field_data)
    
    def setEnumeration(self, field, field_data):
                   
        enum_class_name = self._osi.getFieldType(self._object_type, field)
        module_name = self._osi.getClassModuleName(enum_class_name)
        
        module = importlib.import_module(module_name)
        enum_wrapper = operator.attrgetter(enum_class_name)(module)
        
        setattr(self._osi_object,
                field, 
                enum_wrapper.Value(field_data))


    def getOsi(self):
        """Return reference to the osi object"""
        return self._osi_object

    def serializeToString(self):
        """Return serialized protobuf string """
        return self._osi_object.SerializeToString()

    def print(self):
        print(type(self._osi_object))
        print(self._osi_object)



def readJSON(file_name):
    """ Read JSON file from disk"""
    with open(file_name) as f:
        data = json.load(f)
    return data

def writeStringToFile(file_name, string):
    """Dumps string to file"""
    with open(file_name, 'wb') as f:
        f.write(string)


def main():
    """Main Function of the program"""

    # Define Comand Line Interface
    parser = argparse.ArgumentParser(
                description="Converts input defined in JSON format and output osi binary file with a single message. ")
    parser.add_argument('input_json',
                help='Input file defining osi object in JSON format.',
                type=str)
    parser.add_argument('output_osi',
                help='Output file name for encoded osi object.',
                type=str)
    parser.add_argument('osi_class_name',
                help='Name of the class passed in input file',
                type=str)

    # Handle comand line argiuments
    args = parser.parse_args()
    input_json_file = args.input_json
    input_class_name = args.osi_class_name
    output_osi_file = args.output_osi

    # Create OSI data structure 
    osi_structure = OsiStructure()
    creator = OsiJsonCreator(osi_structure, input_class_name)
    creator.buildFromJSON(readJSON(input_json_file))

    # Inspect data structure
    creator.print()
    print(type(creator.serializeToString()))

    # Write to file
    writeStringToFile(output_osi_file, creator.serializeToString())

if __name__ == "__main__":
    main()
