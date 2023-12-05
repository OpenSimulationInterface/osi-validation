"""Module for test class of OSIValidationRules class"""

import unittest

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule


class TestIsGreaterThan(unittest.TestCase):
    """Test for rule is_greater_than"""

    def setUp(self):
        self.FRC = OSIRulesChecker()

    def tearDown(self):
        del self.FRC

    def test_comply_greater(self):
        field_params_rule_params = [
            [2, 1],
            [0, -1],
            [1, 0],
            [1, -1],
            [-1, -2],
            [-1.3, -1.5],
            [0.9, -1.3],
        ]

        for fr_param in field_params_rule_params:
            with self.subTest(fr_param=fr_param):
                self.assertTrue(
                    self.FRC.is_greater_than(
                        LinkedProtoField(value=fr_param[0]),
                        Rule(verb="is_greater_than", params=fr_param[1]),
                    )
                )

    def test_not_comply_greater(self):
        field_params_rule_params = [
            [2, 1],
            [0, -1],
            [1, 0],
            [1, -1],
            [-1, -2],
            [-1.3, -1.5],
            [0.9, -1.3],
        ]

        for fr_param in field_params_rule_params:
            with self.subTest(fr_param=fr_param):
                self.assertFalse(
                    self.FRC.is_greater_than(
                        LinkedProtoField(value=fr_param[1]),
                        Rule(verb="is_greater_than", params=fr_param[0]),
                    )
                )

    def test_not_comply_equal(self):
        field_params_rule_params = [[3, 3], [0, 0], [-1, -1], [-1.5, -1.5], [2.3, 2.3]]

        for fr_param in field_params_rule_params:
            with self.subTest(fr_param=fr_param):
                self.assertFalse(
                    self.FRC.is_greater_than(
                        LinkedProtoField(value=fr_param[1]),
                        Rule(verb="is_greater_than", params=fr_param[0]),
                    )
                )
