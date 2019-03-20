#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The lines above make sure that the first python3 interpreter in your path is used for the execution.
# And that the correct encoding is used

import argparse
from pyosi.reading import separate_all_sections
from pyosi.reading import decode_data
from pyosi.reading import read_text_data


    encoded_data = read_text_data(EXAMPLE_FILE)
    separated_data = separate_all_sections(encoded_data)
    data_class = osi3.osi_sensorview_pb2.SensorView
    decoded_data = decode_data(separated_data, data_class)

def main():
    
    parser = argparse.ArgumentParser(description='Process OSI 3.0.0 protobuff binary file')
    parser.add_argument('input_filename', help='Series of OSI messages endoded to osi_bytes')
    parser.add_argument('output_filename', help='Output filename')
    args = parser.parse_args()
    
    with open(args.input_filename, "rb") as f:
        input_data = f.read()
    print(args)
    print('Length of data {}'.format(len(input_data)))

    data_encoded = separate_all_sections(input_data)

    data_class = osi3.osi_sensorview_pb2.SensorView
    decoded_data = decode_data(data_encoded, data_class)



if __name__ == '__main__':
    main()