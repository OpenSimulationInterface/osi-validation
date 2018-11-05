# import local libabries
import osi3.osi_groundtruth_pb2
import osi3.osi_sensorview_pb2


# OPen and Read text file 
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
            print('NO MORE SEPARATORS')
            return result 
            
        result.append(encoded[start:end])
        start = end + len(SEPARATOR)

    return result

# Decoder 
def decode_data(encoded_data, data_class):
    decoded_data = []
    for row in encoded_data:
        data_object = data_class()
        data_object.ParseFromString(row)
        decoded_data.append(data_object)
    return decoded_data

# Timestamp by timestamp

# Main
def main():
    #EXAMPLE_FILE = './Example_Data/CornerRoadObjects_mini/CornerRoadExample_SensorData.txt'
    EXAMPLE_FILE = './Example_Data/CornerRoadObjects_mini/CornerRoadObjects_mini.txt' 
    
    encoded_data = read_text_data(EXAMPLE_FILE)
    separated_data = separate_all_sections(encoded_data)
    data_class = osi3.osi_sensorview_pb2.SensorView
    decoded_data = decode_data(separated_data, data_class)
    

# Entry point
if __name__ == '__main__':
    main()