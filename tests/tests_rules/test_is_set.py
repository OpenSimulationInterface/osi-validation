"""
Module for test class of is_set rule implementation

Test-tree:

    Orientation3d
          |
    -------------
    |     |     |
   roll pitch  yaw
    1    None   2

Complying tests:
- set roll and check is_set == True
- set yaw and check is_set == True

Not complying test:
- don't set pitch check is_set == False

"""

import unittest

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule
from osi3.osi_common_pb2 import Orientation3d


class TestIsSet(unittest.TestCase):
    def setUp(self):
        self.FRC = OSIRulesChecker()

        pb_ORIENTATION3D = Orientation3d()
        pb_ORIENTATION3D.roll = 1
        # pb_ORIENTATION3D.pitch = 2 --> pitch is not set
        pb_ORIENTATION3D.yaw = 2
        self.ORIENTATION3D = LinkedProtoField(pb_ORIENTATION3D, "Orientation3d")

    def tearDown(self):
        del self.FRC
        del self.ORIENTATION3D

    def test_comply_is_set(self):
        rule = Rule(verb="is_set", field_name="roll")
        compliance = self.FRC.is_set(self.ORIENTATION3D, rule)
        self.assertTrue(compliance)

        rule = Rule(verb="is_set", field_name="yaw")
        compliance = self.FRC.is_set(self.ORIENTATION3D, rule)
        self.assertTrue(compliance)

    def test_comply_is_not_set(self):
        rule = Rule(verb="is_set", field_name="pitch")
        compliance = self.FRC.is_set(self.ORIENTATION3D, rule)
        self.assertFalse(compliance)
