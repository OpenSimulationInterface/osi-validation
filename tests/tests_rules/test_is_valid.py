"""Module for test class of OSIValidationRules class"""

import unittest

from osi3.osi_common_pb2 import Orientation3d

from linked_proto_field import LinkedProtoField
from osi_rules import (
    Rule,
    TypeRulesContainer,
    ProtoMessagePath,
    MessageTypeRules,
    FieldRules,
)

from osi_rules_checker import OSIRulesChecker


class TestIsValid(unittest.TestCase):
    def setUp(self):
        self.FRC = OSIRulesChecker()
        orient3d = Orientation3d()
        orient3d.roll = 5
        orient3d.pitch = 2
        orient3d.yaw = 2
        self.linked_orient3d = LinkedProtoField(orient3d, "Orientation3d")

    def tearDown(self):
        del self.FRC
        del self.linked_orient3d

    def test_comply_is_valid(self):
        container = TypeRulesContainer()
        proto_path = ProtoMessagePath(["Orientation3d", "roll"])
        container.add_type_from_path(proto_path)

        root_container = TypeRulesContainer()
        root_path = ProtoMessagePath(["Orientation3d"])
        root_container.add_type_from_path(root_path)

        rule1 = Rule(
            verb="is_greater_than",
            field_name="roll",
            params=0,
            path=proto_path,
            extra_params=dict(),
        )
        rule2 = Rule(
            verb="is_less_than",
            field_name="roll",
            params=10,
            path=proto_path,
            extra_params=dict(),
        )

        rules = FieldRules(
            "roll", rules=[rule1, rule2], path=proto_path, root=root_container
        )

        rule = MessageTypeRules(name="Orientation3d")
        rule.add_field(rules)
        rule.add_type_from_path(rules)

        rule.root = container
        rule._path = proto_path
        rule.path = proto_path

        compliance = self.FRC.is_valid(self.linked_orient3d, rule)
        self.assertTrue(compliance)

    def test_comply_is_not_valid(self):
        container = TypeRulesContainer()
        proto_path = ProtoMessagePath(["Orientation3d", "roll"])
        container.add_type_from_path(proto_path)

        root_container = TypeRulesContainer()
        root_path = ProtoMessagePath(["Orientation3d"])
        root_container.add_type_from_path(root_path)

        rule1 = Rule(
            verb="is_greater_than",
            field_name="roll",
            params=6,
            path=proto_path,
            extra_params=dict(),
        )
        rule2 = Rule(
            verb="is_less_than",
            field_name="roll",
            params=10,
            path=proto_path,
            extra_params=dict(),
        )

        rules = FieldRules(
            "roll", rules=[rule1, rule2], path=proto_path, root=root_container
        )

        rule = MessageTypeRules(name="Orientation3d")
        rule.add_field(rules)
        rule.add_type_from_path(rules)

        rule.root = container
        rule._path = proto_path
        rule.path = proto_path

        compliance = self.FRC.is_valid(self.linked_orient3d, rule)
        self.assertFalse(compliance)
