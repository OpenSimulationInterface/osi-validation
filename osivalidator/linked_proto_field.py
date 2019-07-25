"""
This class describe a wrapper on protobuf fields that add a link
with parent message and bind message to its field descriptor (when the
message is nested).
"""

from google.protobuf.message import Message
from google.protobuf.pyext._message import RepeatedCompositeContainer


class LinkedProtoField:
    """
    This class describe a wrapper on protobuf fields that add a link
    with parent message and bind message to its field descriptor (when the
    message is nested).

    The Protobuf's RepeatedCompositeContainer that describes repeated field are
    replaced with Python lists.
    The field informations (parent message and field name) for the repeated
    field are here bounded to each element of the list.
    """

    def __init__(self, proto_node, field_name=None, parent=None):
        self._proto_field_name = field_name
        self._proto_node = proto_node
        self._parent = parent

    def GetProtoNode(self):
        """
        Return the deserialized protobuf data, i.e. if the node wrap a message,
        it will yield a message, if it is a native type it will return the
        value.
        """
        return self._proto_node

    def GetFieldName(self):
        """
        Return the name of the field in its parent message.
        """
        return self._proto_field_name

    def GetParent(self):
        """
        Return the parent message as a LinkedProtoField.
        """
        return self._parent

    def ListFields(self):
        """
        Overloading of protobuf ListFields function that return
        a list of LinkedProtoFields.

        Only works if the field is composite, raise an AttributeError otherwise.
        """
        return [
            LinkedProtoField(field_tuple[1], parent=self,
                             field_name=field_tuple[0].name)
            for field_tuple in self._proto_node.ListFields()
        ]

    def IsMessage(self):
        """
        Return true if the field contains a message.
        """
        return isinstance(self._proto_node, Message)

    def GetField(self, field_name):
        """
        If the LinkedProtoField wraps a message, return the field of this
        message. Otherwise, raise an AttributeError.
        """
        field = getattr(self._proto_node, field_name)
        return LinkedProtoField(field, parent=self, field_name=field_name)

    def __getattr__(self, attr_name):
        if attr_name in ['__getstate__', '__setstate__']:
            return object.__getattr__(self, attr_name)

        if attr_name in "_proto_message":
            raise AttributeError("Undesirable recursion")

        attr = getattr(self._proto_node, attr_name)

        if isinstance(attr, Message):
            return self.GetField(attr_name)
        if isinstance(attr, RepeatedCompositeContainer):
            return [
                LinkedProtoField(field, parent=self, field_name=attr_name)
                for field in attr
            ]

        return attr

    def __repr__(self):
        return self._proto_node.__repr__()

    def __float__(self):
        return float(self._proto_node)

    def __getitem__(self, field_name):
        return self.GetField(field_name)
