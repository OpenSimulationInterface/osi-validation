"""
Module for test class of Check-if rule implementation

Test-tree:

      Vector3d
          |
    -------------
    |     |     |
    x     y     z
    1     2    None

Complying tests:
- if y == 3, check x == 2 
- if y == 2, check x == 1
- if y == 2, check x is_set == True

Not complying test:
- if y == 2, check x == 2
- if y == 2, check z is_set == False

"""

import unittest
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule
from osivalidator.osi_rules_checker import OSIRulesChecker

from osi3.osi_common_pb2 import Vector3d


class TestCheckIf(unittest.TestCase):
    """Test class of OSI Rule check_if class"""

    def setUp(self):
        self.FRC = OSIRulesChecker()

        pb_VECTOR3D = Vector3d()
        pb_VECTOR3D.x = 1
        pb_VECTOR3D.y = 2
        self.VECTOR3D = LinkedProtoField(pb_VECTOR3D, "Vector3D")

    def test_comply1(self):
        rule = Rule(
            verb="check_if",
            field_name="x",
            params=[{"is_equal_to": 3, "target": "this.y"}],
            extra_params={"do_check": [{"is_equal_to": 2}]},
        )
        compliance = self.FRC.check_if(self.VECTOR3D, rule)
        self.assertTrue(compliance)

    def test_comply2(self):
        rule = Rule(
            verb="check_if",
            field_name="x",
            params=[{"is_equal_to": 2, "target": "this.y"}],
            extra_params={"do_check": [{"is_equal_to": 1}]},
        )
        compliance = self.FRC.check_if(self.VECTOR3D, rule)
        self.assertTrue(compliance)

    def test_comply_is_set(self):
        rule = Rule(
            verb="check_if",
            field_name="x",
            params=[{"is_equal_to": 2, "target": "this.y"}],
            extra_params={"do_check": [{"is_set": None}]},
        )
        compliance = self.FRC.check_if(self.VECTOR3D, rule)
        self.assertTrue(compliance)

    def test_not_comply(self):
        rule = Rule(
            verb="check_if",
            field_name="x",
            params=[{"is_equal_to": 2, "target": "this.y"}],
            extra_params={"do_check": [{"is_equal_to": 2}]},
        )
        compliance = self.FRC.check_if(self.VECTOR3D, rule)
        self.assertFalse(compliance)

    def test_not_comply_is_set_if(self):
        rule = Rule(
            verb="check_if",
            field_name="z",
            params=[{"is_equal_to": 2, "target": "this.y"}],
            extra_params={"do_check": [{"is_set": None}]},
        )
        compliance = self.FRC.check_if(self.VECTOR3D, rule)
        self.assertFalse(compliance)
