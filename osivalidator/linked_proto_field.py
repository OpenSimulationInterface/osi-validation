"""
This class describe a wrapper on protobuf fields that add a link
with parent message and bind message to some additional informations.
"""

from google.protobuf.message import Message
from google.protobuf.pyext._message import RepeatedCompositeContainer
from google.protobuf.json_format import MessageToDict


class LinkedProtoField:
    """
    This class describe a wrapper on protobuf fields that add a link
    with parent message and bind message to some additional informations.

    The Protobuf's RepeatedCompositeContainer that describes repeated field are
    replaced with Python lists.
    The field informations (parent message and field name) for the repeated
    field are here bounded to each element of the list.
    """

    def __init__(self, value, name=None, parent=None):
        self.name = name
        self.value = value
        self.parent = parent
        self.is_message = isinstance(self.value, Message)
        self.path = name if parent is None else parent.path + "." + name

        self._dict = None
        self._fields = None

    @property
    def dict(self):
        """
        Return the dict version of the protobuf message.

        Compute the dict only once, then store it and retrieve it.
        """
        if self._dict is None:
            self._dict = MessageToDict(self.value)

        return self._dict

    def _retrieve_fields(self):
        self._fields = {field_tuple[0].name:
                        LinkedProtoField(field_tuple[1], parent=self,
                                         name=field_tuple[0].name)
                        for field_tuple in self.value.ListFields()}

    @property
    def fields(self):
        """
        Overloading of protobuf ListFields function that return
        a list of LinkedProtoFields.

        Only works if the field is composite, raise an AttributeError otherwise.
        """
        if self._fields is None:
            self._retrieve_fields()

        return self._fields.values()

    def get_field(self, field_name):
        """
        If the LinkedProtoField wraps a message, return the field of this
        message. Otherwise, raise an AttributeError.
        """
        if self._fields is not None:
            return self._fields[field_name]

        field = getattr(self.value, field_name)
        return LinkedProtoField(field, parent=self, name=field_name)

    def has_field(self, field_name):
        """
        Check if a protobuf message message have an attribute/field even if this
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

    def query(self, path):
        """
        Return a LinkedProtoField from a path.

        Example of path: ./global_ground_truth/moving_object
        """
        cursor = self
        for path_component in path.split("/"):
            if path_component == ".":
                cursor = cursor
            elif path_component == "..":
                cursor = cursor.parent
            else:
                cursor = cursor.get_field(path_component)
        return cursor

    def __repr__(self):
        return self.value.__repr__()
