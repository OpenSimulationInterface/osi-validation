def timestamp_string_value(timestamp):
    """ String representation of osi timestamp"""
    return '{:d}.{:09d}'.format(timestamp.seconds, timestamp.nanos)
