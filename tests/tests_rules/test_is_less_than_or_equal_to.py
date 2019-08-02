"""Module for test class of OSIValidationRules class"""

import sys
import unittest
from collections import namedtuple
from osivalidator.osi_rules_implementations import is_less_than_or_equal_to
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule


sys.path.append("../..")

FRC = namedtuple('fake_rule_checker', ['log'])(log=lambda x, y: True)


class TestIsLessThanOrEqualTo(unittest.TestCase):
    """Test class of OSIDataContainer class"""

    def test_comply(self):
        field = LinkedProtoField(value=1)
        rule = Rule(verb="is_less_than_or_equal_to", params=2)
        compliance = is_less_than_or_equal_to(None, field, rule)
        self.assertTrue(compliance)

    def test_not_comply(self):
        field = LinkedProtoField(value=3)
        rule = Rule(verb="is_less_than_or_equal_to", params=2)
        compliance = is_less_than_or_equal_to(FRC, field, rule)
        self.assertFalse(compliance)
