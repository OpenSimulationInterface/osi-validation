"""Module for test class of OSIValidationRules class"""

import sys
import unittest

from osi3.osi_common_pb2 import Orientation3d

from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule, TypeRulesContainer

from osivalidator.osi_scenario import OSIScenario
from osivalidator.osi_rules import OSIRules
from osivalidator.osi_validator_logger import OSIValidatorLogger
from osivalidator.osi_rules_checker import OSIRulesChecker


sys.path.append("../..")


# TODO Implement this (This checking is a little bit more complex)
class TestIsValid(unittest.TestCase):

    def setUp(self):
        self.FRC = OSIRulesChecker()

        pb_ORIENTATION3D = Orientation3d()
        pb_ORIENTATION3D.roll = 1
        pb_ORIENTATION3D.pitch = 2
        pb_ORIENTATION3D.yaw = 2
        self.ORIENTATION3D = LinkedProtoField(pb_ORIENTATION3D, "Orientation3d")

    def tearDown(self):
        del self.FRC
        del self.ORIENTATION3D

    def test_comply_is_valid(self):
        rule = Rule(verb="is_greater_than", field_name='roll',  params=0)
        compliance = self.FRC.is_valid(self.ORIENTATION3D, rule)
        self.assertTrue(compliance)

    def test_comply_is_not_valid(self):
        rule = Rule(verb="is_set", field_name="pitch")
        compliance = self.FRC.is_valid(self.ORIENTATION3D, rule)
        self.assertFalse(compliance)
