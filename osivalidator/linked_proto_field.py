"""
This class describes a wrapper on protobuf fields that add a link
with parent message and bind message to some additional information.
"""

from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import osi_rules


class LinkedProtoField:
    """
    This class describes a wrapper on protobuf fields that add a link
    with parent message and bind message to some additional information.

    The Protobuf's RepeatedCompositeContainer that describes repeated field are
    replaced with Python lists.
    The field information (parent message and field name) for the repeated
    field are here bounded to each element of the list.
    """

    def __init__(self, value, name=None, parent=None):
        self.name = name
        self.value = value
        self.parent = parent
        self.path = name if parent is None else parent.path + "." + name

        self._dict = None
        self._fields = None
        self._message_type = None

    @property
    def is_message(self):
        """Return true if the field contain a message"""
        return isinstance(self.value, Message)

    @property
    def message_type(self):
        """
        Return a path to the message type in OSI3 as a ProtoMessagePath
        """
        if not self._message_type:
            field_type_desc = self.value.DESCRIPTOR
            message_type = []
            while field_type_desc is not None:
                message_type.insert(0, field_type_desc.name)
                field_type_desc = field_type_desc.containing_type
            self._message_type = osi_rules.ProtoMessagePath(message_type)
        return self._message_type

    @property
    def fields(self):
        """
        Overloading of protobuf ListFields function that return
        a list of LinkedProtoFields.

        Only works if the field is composite, raise an AttributeError otherwise.
        """
        if self._fields is None:
            self._fields = {
                field_tuple[0].name: self.get_field(field_tuple[0].name)
                for field_tuple in self.value.ListFields()
            }

        return self._fields.values()

    @property
    def all_field_descriptors(self):
        """
        List all the fields descriptors, i.e even the one that are not set
        """
        return self.value.DESCRIPTOR.fields

    def to_dict(self):
        """
        Return the dict version of the protobuf message.

        Compute the dict only once, then store it and retrieve it.
        """
        if self._dict is None:
            self._dict = MessageToDict(self.value)

        return self._dict

    def get_field(self, field_name):
        """
        If the LinkedProtoField wraps a message, return the field of this
        message. Otherwise, raise an AttributeError.
        """
        if self._fields is not None:
            return self._fields[field_name]

        field = getattr(self.value, field_name)

        if (
            hasattr(self.value, "DESCRIPTOR")
            and self.value.DESCRIPTOR.fields_by_name[field_name].label == 3
        ):
            return [
                LinkedProtoField(u_field, parent=self, name=field_name)
                for u_field in field
            ]

        return LinkedProtoField(field, parent=self, name=field_name)

    def has_field(self, field_name):
        """
        Check if a protobuf message has an attribute/field even if this
        is a repeated field.

        If it is a repeated field, this function returns false if there is no
        element into it.
        """
        try:
            return self.value.HasField(field_name)
        except ValueError:
            try:
                return len(getattr(self.value, field_name)) > 0
            except AttributeError:
                return False

    def query(self, path, parent=False):
        """
        Return a LinkedProtoField from a path.

        Example of path: ./global_ground_truth/moving_object
        """
        cursor = self
        components = path.split(".")
        if parent:
            if len(components) > 1:
                components.pop()
            else:
                components.append("parent")

        for path_component in components:
            if path_component == "this":
                cursor = cursor
            elif path_component == "parent":
                cursor = cursor.parent
            else:
                cursor = cursor.get_field(path_component)

        return cursor

    def __repr__(self):
        return self.value.__repr__()
