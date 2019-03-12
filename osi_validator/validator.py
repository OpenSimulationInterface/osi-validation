#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# Use imports above in anty python2 code

from copy import copy
import logging
import datetime
import argparse

from validation.stationary_object import StationaryObjectValidator
from validation.moving_object import MovingObjectVaidator
from validation.traffic_sign import TrafficSignValidator
from validation.traffic_light import TrafficLightValidator
from validation.occupant import OccupantValidator
from validation.road_marking import RoadMarkingValidator
from validation.environment import EnvironmentalConditionsValidator

from validation.ground_truth import GroundTruthValidator

import validation.lane as lane

import osi3.osi_groundtruth_pb2
import osi3.osi_sensorview_pb2


# Basic setup for logger
class DefineLoggers():
    """ Define Stream and File logger """
   
    log = logging.getLogger('v_osi')
    log.setLevel(logging.INFO)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    @classmethod
    def set_log_level(cls, level):
        if level == 'debug': cls.log.setLevel(logging.DEBUG)
        if level == 'info': cls.log.setLevel(logging.INFO)
        if level == 'warning': cls.log.setLevel(logging.WARNING)

    @classmethod
    def activate_file_log(cls, filename = None):
        """ Create and configure FileHandler"""
        if filename is None:
            filename = 'osi_v.log'
        fh = logging.FileHandler(filename, mode='w')
        fh.setFormatter(cls.formatter)
        cls.log.addHandler(fh)
   
    @classmethod   
    def activate_stream_log(cls):
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setFormatter(cls.formatter)
        cls.log.addHandler(ch)

# Open and Read text file 
def read_text_data(file_name):
    with open(file_name, "rb") as f:
        data = f.read()
    return data

# Search for separators 
def separate_all_sections(encoded):
    """ Separate files based on  """
    SEPARATOR = b'$$__$$'
    result = []
    start, end = 0, 0

    is_finished = False 
    while not is_finished:
        end = encoded.find(SEPARATOR, start)

        # Finishing coverage
        if end == -1:
            is_finished = True
            return result 
            
        result.append(encoded[start:end])
        start = end + len(SEPARATOR)

    return result

# Decode protobuff data
def decode_data(encoded_data, data_class):
    decoded_data = []
    for row in encoded_data:
        data_object = data_class()
        data_object.ParseFromString(row)
        decoded_data.append(data_object)
    return decoded_data

def real_data_trial():
    EXAMPLE_FILE = './Data/overtake_right_straight_SensorView.txt' 
    
    encoded_data = read_text_data(EXAMPLE_FILE)
    separated_data = separate_all_sections(encoded_data)
    data_class = osi3.osi_sensorview_pb2.SensorView
    decoded_data = decode_data(separated_data, data_class)
    step = take_one_timestamp(decoded_data)
    validate_ground_truth(step.global_ground_truth)

def validate_ground_truth(data):
    print(osi_version2string(data.version))
    print(osi_timestamp2string(data.timestamp))
    print('Host Vehicle ID : {}'.format(data.host_vehicle_id.value))
    print('Number of objects stationary_object : {}'.format(len(data.stationary_object)))
    print('Number of objects moving_object : {}'.format(len(data.moving_object)))
    print('Number of objects traffic_sign : {}'.format(len(data.traffic_sign)))
    print('Number of objects traffic_light : {}'.format(len(data.traffic_light)))
    print('Number of objects road_marking : {}'.format(len(data.road_marking)))
    print('Number of objects lane_boundary : {}'.format(len(data.lane_boundary)))
    print('Number of objects lane : {}'.format(len(data.lane)))
    print('Number of objects occupant : {}'.format(len(data.occupant)))
    print('Curret time in simulation enviroment : {}'.format(datetime.timedelta(seconds=data.environmental_conditions.time_of_day.seconds_since_midnight)))
    print('---------------------------------------------')

    ggv = GroundTruthValidator()
    ggv.load_data(data)
    ggv.context = 'Ground Truth'
    ggv.validate()

def osi_version2string(version):
    """ String represntation of OSI version """
    return 'OSI Version : {}.{}.{}'.format(version.version_major, version.version_minor, version.version_patch)

def osi_timestamp2string(timestamp):
    """ String representation of osi timestamp"""
    time = timestamp.seconds + timestamp.nanos/10**9
    return 'Timestamp : {:16.9f}'.format(time)

def take_one_timestamp(data):
    n_steps = len(data)
    middle = n_steps // 2
    return data[middle]

def command_line_arguments():
    # Define Comand Line Interface
    parser = argparse.ArgumentParser(
                description="Validate OSI protobuf message.")
    #parser.add_argument('input_osi_binary_text',
    #            help='Input file containing OSI encoded as a binary text.',
    #            type=str)
    parser.add_argument('--log_level',
                choices=['error','warning','info','debug'],
                help='Define loging lever for the programm',
                type=str,
                required=False)
    # Handle comand line argiuments
    return parser.parse_args()

def main():
    real_data_trial()

print('Script started')
if __name__ == "__main__":
    arguments = command_line_arguments()
    DefineLoggers().activate_stream_log()
    DefineLoggers().activate_file_log()
    
    if arguments.log_level is not None:
        print(arguments.log_level)
        DefineLoggers().set_log_level(arguments.log_level)
    
    
    main()
