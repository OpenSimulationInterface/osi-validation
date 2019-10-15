"""Module for test class of OSIValidationRules class"""

import unittest

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule


class TestIsEqual(unittest.TestCase):
    """Test class of OSIDataContainer class"""

    def setUp(self):
        self.FRC = OSIRulesChecker()

    def tearDown(self):
        del self.FRC

    def test_comply(self):
        field = LinkedProtoField(value=2)
        rule = Rule(verb="is_less_than_or_equal_to", params=2)
        compliance = self.FRC.is_equal_to(field, rule)
        self.assertTrue(compliance)

    def test_not_comply(self):
        field = LinkedProtoField(value=3)
        rule = Rule(verb="is_less_than_or_equal_to", params=2)
        compliance = self.FRC.is_equal_to(field, rule)
        self.assertFalse(compliance)
