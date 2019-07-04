"""
Here are the useful functions that can be used in differents modules.
"""


def get_message_path(inherit):
    """Return the path to a message from the inheritance list of the message.
    """
    not_none_elt = filter(lambda i: i[0] is not None, inherit)
    return ".".join(map(lambda i: i[0].name, not_none_elt))


def has_attr(message, field_name):
    """
    Check if a protobuf message message have an attribute/field even if this is
    a repeated field.

    If it is a repeated field, this function returns false if there is no
    element into it.
    """
    try:
        return message.HasField(field_name)
    except ValueError:
        try:
            return len(getattr(message, field_name)) > 0
        except AttributeError:
            return False


def get_size_from_file_stream(file_object):
    current_position = file_object.tell()
    file_object.seek(0, 2)
    size = file_object.tell()
    file_object.seek(current_position)
    return size
