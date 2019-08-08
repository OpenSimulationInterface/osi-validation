"""Module for test class of OSIValidationRules class"""

import sys
import unittest
from collections import namedtuple
#from osivalidator.osi_rules_implementations import first_element
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule

sys.path.append("../..")


class TestFirstElement(unittest.TestCase):

    def setUp(self):
        FRC = namedtuple('fake_rule_checker', ['log'])
        self.fake_rule_checker = FRC(log=lambda x, y: True)

    # TODO Implement this
    def test_comply_first_element(self):
        from osivalidator.osi_rules_implementations import first_element
        self.assertTrue(
                first_element(self.fake_rule_checker, 
                                            LinkedProtoField(value=1), 
                                            Rule(verb="first_element", params=2))
                                            )
