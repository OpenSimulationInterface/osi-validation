#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import osi3.osi_sensorview_pb2
import pandas as pd
import argparse

def separator_gen(encoded):
    """ Separate files based on  """
    SEPARATOR = b'$$__$$'
    start, end = 0, 0

    is_finished = False 
    while not is_finished:
        end = encoded.find(SEPARATOR, start)

        # Finishing coverage
        if end == -1:
            is_finished = True
            end = len(encoded)
            
        if len(encoded[start:end]) == 0:
            print('Data stream finished with a separator')
            break
        yield encoded[start:end]
        start = end + len(SEPARATOR)

def parser_gen(separator_gen, data_class):
    for data in separator_gen:
        parsed = data_class()
        parsed.ParseFromString(data)
        yield parsed
        
def timestamp_string_value(timestamp):
    """ String representation of osi timestamp"""
    return '{:d}.{:09d}'.format(timestamp.seconds, timestamp.nanos)

def main():
    
    parser = argparse.ArgumentParser(description='Process OSI 3.0.0 protobuff binary file')
    parser.add_argument('input_filename', help='Series of OSI messages endoded to osi_bytes')
    parser.add_argument('output_filename', help='Output filename')
    args = parser.parse_args()
    
    # Grab data from file 
    with open(args.input_filename , "rb") as openfile: input_data = openfile.read()


    file = 'ASTAS_Trace_with_timestamps.txt'   
    with open(file , "rb") as openfile: input_data = openfile.read()

    separator = separator_gen(input_data)
    data_class = osi3.osi_sensorview_pb2.SensorView

    # Grab all timestamps form messages and insert info a DataFrame
    ser = list()

    for msg in parser_gen(separator, data_class):
        ser.append(float(timestamp_string_value(msg.timestamp)))
    
    delta = [b - a  for a, b  in zip(ser, ser[1::])]

    with open('output.txt','w') as f:
        f.write('Deltas')
        for element in delta:
            f.write(str(element) + '\n')

    # Write dataframe to CSV
    # ser.to_csv('timestamps.csv', sep=',', encoding='utf-8')


if __name__ == '__main__':
    main()

# osi_featuredata.proto:    optional Timestamp measurement_time = 1;
# osi_groundtruth.proto:    optional Timestamp timestamp = 2;
# osi_sensordata.proto:    optional Timestamp measurement_time = 1;
# osi_sensordata.proto:    optional Timestamp timestamp = 2;
# osi_sensordata.proto:    optional Timestamp last_measurement_time = 9;
# osi_sensorviewconfiguration.proto:    optional Timestamp update_cycle_time = 8;
# osi_sensorviewconfiguration.proto:    optional Timestamp update_cycle_offset = 9;
# osi_sensorviewconfiguration.proto:    optional Timestamp simulation_start_time = 10;
# osi_sensorview.proto:    optional Timestamp timestamp = 2;
