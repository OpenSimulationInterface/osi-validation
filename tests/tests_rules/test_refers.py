"""Module for test class of OSIValidationRules class"""

import sys
import unittest
from collections import namedtuple
from osivalidator.osi_rules_implementations import refers
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule

sys.path.append("../..")


class TestRefers(unittest.TestCase):

    def setUp(self):
        FRC = namedtuple('fake_rule_checker', ['log'])
        self.fake_rule_checker = FRC(log=lambda x, y: True)

    # TODO In progress
    def test_comply_refers(self):
        self.assertTrue(
            refers(self.fake_rule_checker,
                   LinkedProtoField(value=1),
                   Rule(verb="refers", params=2))
        )
