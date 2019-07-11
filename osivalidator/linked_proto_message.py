"""
This class describe a wrapper on protobuf messages that add a link with
parent message and bind message to its field descriptor (when the message is
nested).
"""


class LinkedProtoMessage:
    """
    This class describe a wrapper on protobuf messages that add a link with
    parent message and bind message to its field descriptor (when the message is
    nested).
    """

    def __init__(self, proto_message, parent=None, descriptor=None):
        self.proto_message = proto_message
        self.parent = parent
        self.descriptor = descriptor
        self.field_descriptor_value_tuples = None

    def get_field_descriptor_value_tuple_by_name(self, field_name):
        """
        Return only one tuple (FieldDescriptor, value) of the field which
        corresponds to the field name "field_name"
        """
        for field_tuple in self.field_descriptor_value_tuples:
            if field_name == field_tuple[0]:
                return field_tuple

        raise KeyError(self.proto_message.name +
                       ' does not contain any field named "' + field_name + '"')

    def __getattr__(self, attr_name):
        # Generate the field list if not already done
        if self.field_descriptor_value_tuples is None:
            self.field_descriptor_value_tuples = self.proto_message.ListFields()

        try:
            # Try to return a field
            descriptor, value = self.get_field_descriptor_value_tuple_by_name(
                attr_name)
        except KeyError:
            # If no field found, try to return a proto_message field
            # Error will be handled by it
            return getattr(self.proto_message, attr_name)
        else:
            if descriptor.label == 3:
                # If REPEATED field, return a list of LinkedProtoMessage.
                return [
                    LinkedProtoMessage(repeated_value, self, descriptor)
                    for repeated_value
                    in value
                ]

            # else, return a simple LinkedProtoMessage
            return LinkedProtoMessage(value, self, descriptor)
