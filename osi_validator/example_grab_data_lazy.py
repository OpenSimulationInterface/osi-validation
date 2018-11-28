#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

import osi3.osi_sensorview_pb2
from  pyosi.reading_lazy import separate_all_sections, decode_data, read_text_data
        
def timestamp_string_value(timestamp):
    """ String representation of osi timestamp"""
    return '{:d}.{:09d}'.format(timestamp.seconds, timestamp.nanos)

# Grab data from file 
file = './Data/ASTAS_Trace_with_timestamps.sosibytes'
input_data = read_text_data(file)

# Data class
data_class = osi3.osi_sensorview_pb2.SensorView

# Separate 
separator = separate_all_sections(input_data)

df = pd.DataFrame()

# Grab all timestamps form messages and insert info a DataFrame
for i, msg in enumerate(decode_data(separator, data_class)):
    print(timestamp_string_value(msg.timestamp))
    data = {
    'message_number' : i,
    'SV_timestamp_nanos' : msg.timestamp.seconds * 10 ** 9 + msg.timestamp.nanos,
    'GT_timestamp_nanos' : msg.global_ground_truth.timestamp.seconds * 10 ** 9 + \
                     msg.global_ground_truth.timestamp.nanos,
    'n_stationary_objects' : len(msg.global_ground_truth.stationary_object),
    'n_moving_objects' : len(msg.global_ground_truth.moving_object),
    'n_traffic_signs' : len(msg.global_ground_truth.traffic_sign),
    'n_traffic_lights' : len(msg.global_ground_truth.traffic_light),
    'n_road_markings' : len(msg.global_ground_truth.road_marking),
    'n_lane_boundarys' : len(msg.global_ground_truth.lane_boundary),
    'n_lanes' : len(msg.global_ground_truth.lane),
    'n_occupants' : len(msg.global_ground_truth.occupant)}
    msg.
    df = df.append(data, ignore_index=True)

df = df.set_index('message_number')

# Compute a difference between 
df_diff = df.diff()  
df['SV_timestamp_diff_nanos'] = df_diff.SV_timestamp_nanos
df['GT_timestamp_diff_nanos'] = df_diff.GT_timestamp_nanos
df =df.fillna(value=0)

df.info()
df.to_csv('deserialized_ASTAS_Trace_with_timestamps.log')
