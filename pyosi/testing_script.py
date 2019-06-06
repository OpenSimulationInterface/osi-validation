#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import osi3.osi_sensorview_pb2
# import reading


# def main():
    
#     example_data_file = '/home/cszyszka/projects/osi/osi-validation/Data/overtake_right_straight_SensorView.txt'

#     data_class = osi3.osi_sensorview_pb2.SensorView

#     binary_data = reading.read_text_data(example_data_file)
#     generator_separator = reading.separate_all_sections(binary_data)
#     list_of_data = reading.decode_data(generator_separator, data_class)

#     print(f'Data file {example_data_file} contained {len(list_of_data)} timestamps.')


# if __name__ == '__main__':
#     main()
