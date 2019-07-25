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

    def __init__(self, proto_node, field_name=None, parent=None):
        self._proto_field_name = field_name
        self._proto_node = proto_node
        if parent is None:
            self._path = field_name
        else:
            self._path = parent.GetPath() + "." + field_name
        self._parent = parent
        self._dict = None

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

    def GetPath(self):
        """
        Return the path of the field in the message tree.
        """
        return self._path

    def GetDict(self):
        """
        Return the dict version of the protobuf message.

        Compute the dict only once, then store it and retrieve it.
        """
        if self._dict is None:
            self._dict = MessageToDict(self._proto_node)

        return self._dict

    def ListFields(self):
        """
        Overloading of protobuf ListFields function that return
        a list of LinkedProtoFields.

        Only works if the field is composite, raise an AttributeError otherwise.
        """
        return [LinkedProtoField(field_tuple[1], parent=self,
                                 field_name=field_tuple[0].name)
                for field_tuple in self._proto_node.ListFields()]

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

    def HasField(self, field_name):
        """
        Check if a protobuf message message have an attribute/field even if this
        is a repeated field.

        If it is a repeated field, this function returns false if there is no
        element into it.
        """
        try:
            return self._proto_node.HasField(field_name)
        except ValueError:
            try:
                return len(getattr(self._proto_node, field_name)) > 0
            except AttributeError:
                return False

    def __getattr__(self, attr_name):
        if attr_name in ['__getstate__', '__setstate__']:
            return object.__getattr__(self, attr_name)

        if attr_name in "_proto_node":
            raise AttributeError("Undesirable recursion")

        attr = getattr(self._proto_node, attr_name)

        if isinstance(attr, Message):
            return self.GetField(attr_name)

        if isinstance(attr, RepeatedCompositeContainer):
            return [LinkedProtoField(field, parent=self, field_name=attr_name)
                    for field in attr]

        return attr

    def __repr__(self):
        return self._proto_node.__repr__()

    def __float__(self):
        return float(self._proto_node)

    def __getitem__(self, field_name):
        return self.GetField(field_name)
