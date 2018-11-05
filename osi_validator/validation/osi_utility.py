# Collections of wrapers 
# calling protobuff dependent object methods
#
# * referencing releated fields is not wraped as protobuf 
#   implements iterable protocl
import logging
MODULE_LOGGER_NAME         = 'v_osi.osi_utilityies'

# Configure logger for the module
log = logging.getLogger(MODULE_LOGGER_NAME)

def is_set(data, field_name):
	""" Check if field of protobuf is set """
	return data.HasField(field_name)

def is_iterable_set(data, field_name, minimum_length=0):
	""" Check if repeated (iterable in pythonic) field is a minimum length of some value (default biger then 0)"""
	repeated = getattr(data, field_name)
	if len(repeated) > minimum_length:
		return True
	return False

def get_enum_name(enum_wraper, enum_value):
	""" Get string name of enum value"""
	try:
		return enum_wraper.Name(enum_value)
	except ValueError:
		log.error(f'Value {enum_value} is not presnt in {enum_wraper.DESCRIPTOR.full_name}')
		log.error('Possible value-name pairs are')
		for key,value in enum_wraper.items():
			log.error(f'{value} {key}')
		return ''

def get_enum_value(enum_wraper, enum_name):
	""" Get integer value of given enum name"""
	try:
		return enum_wraper.Value(enum_name)
	except ValueError:
		log.error(f'Name {enum_name} is not presnt in {enum_wraper.DESCRIPTOR.full_name}')
		log.error('Possible value-name pairs are')
		for key,value in enum_wraper.items():
			log.error(f'{value} {key}')
		return ''
