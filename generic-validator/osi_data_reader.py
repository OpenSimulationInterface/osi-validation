import osi3 

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
