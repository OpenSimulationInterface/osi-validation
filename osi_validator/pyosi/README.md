# Module pyosi 

Collections of genaral utiliteis for handling OSI messages in python.

## readig_lazy.py
Reading files OSI files that might be very large.

* `read_text_data` - read binray text data
* `separate_all_sections` - separated individual messages assuming b"$$__$$" delimiter.
* `decode_data` - decode data to a specified protobuff class

Example usage is stored in file 
osi-validation/osi_validator/example_grab_data_lazy.py
