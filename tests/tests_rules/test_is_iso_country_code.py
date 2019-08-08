"""Module for test class of OSIValidationRules class"""

import sys
import unittest
from collections import namedtuple
from osivalidator.osi_rules_implementations import is_iso_country_code
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule


sys.path.append("../..")


class TestIsIsoCountryCode(unittest.TestCase):

    def setUp(self):
        FRC = namedtuple('fake_rule_checker', ['log'])
        self.fake_rule_checker = FRC(log=lambda x, y: True)

    # TODO Use Real Field objects
    def test_comply_iso_country_code(self):
        self.assertTrue(
                is_iso_country_code(self.fake_rule_checker, 
                                            'DEU', 
                                            None)
                                            )

    def test_not_comply_iso_country_code(self):
        self.assertFalse(
                is_iso_country_code(self.fake_rule_checker, 
                                            '1234', 
                                            None)
                                            )



