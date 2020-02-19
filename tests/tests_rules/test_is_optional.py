import unittest

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule


class TestIsOptional(unittest.TestCase):
    """
    This Unit test just checks if the rule is_optional is set to True
    because in protobuf 3 every message field is optional
    """

    def setUp(self):
        self.FRC = OSIRulesChecker()

    def tearDown(self):
        del self.FRC

    def test_comply_is_optional(self):
        self.assertTrue(
            self.FRC.is_optional(
                LinkedProtoField(value=1), Rule(verb="is_optional", params=None)
            )
        )
