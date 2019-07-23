"""
This class describe a wrapper on protobuf messages that add a link with
parent message and bind message to its field descriptor (when the message is
nested).
"""

from google.protobuf.message import Message
from google.protobuf.pyext._message import RepeatedCompositeContainer


class LinkedProtoMessage:
    """
    This class describe a wrapper on protobuf messages that add a link with
    parent message and bind message to its field descriptor (when the message is
    nested).
    """

    def __init__(self, proto_node, field_name=None, inheritance=None):
        self._proto_inheritance = inheritance
        self._proto_field_name = field_name
        self._proto_node = proto_node
        self._inheritance = []

    def GetProtoNode(self):
        return self._proto_node

    def GetFieldName(self):
        return self._proto_field_name

    def GetParent(self):
        return self._proto_inheritance[-1]

    def GetPath(self):
        return ".".join(map(lambda node: node.GetFieldName(), self._proto_inheritance))

    def ListFields(self):
        """
        Overloading of protobuf ListFields function that return
        a list of LinkedProtoMessages.
        """
        return [
            LinkedProtoMessage(
                attr_tuple[1],
                inheritance=self._inheritance + [self],
                field_name=attr_tuple[0].name)
            for attr_tuple
            in self._proto_node.ListFields()
        ]

    def IsMessage(self):
        return isinstance(self._proto_node, Message)

    def GetField(self, field_name):
        field = getattr(self._proto_node, field_name)
        return LinkedProtoMessage(
            field,
            inheritance=self._inheritance + [self],
            field_name=field_name
        )

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
                LinkedProtoMessage(
                    single_attr,
                    inheritance=self._inheritance + [self],
                    field_name=attr_name)
                for single_attr
                in attr
            ]

        return attr

    def __repr__(self):
        return self._proto_node.__repr__()

    def __float__(self):
        return float(self._proto_node)

    def __getitem__(self, field_name):
        return self.GetField(field_name)
