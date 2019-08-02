"""
Module for test class of Check-if rule implementation

Test-tree:

   Vector3d
       |
    -------
    |     |
    x     y
    1     2

Complying tests:
- if y == 3, check x == 2 
- if y == 2, check x == 1

Not complying test:
- if y == 2, check x == 2

"""

import sys
import unittest
from osivalidator.osi_rules_implementations import check_if
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule
from osivalidator.osi_rules_checker import OSIRulesChecker
from osi3.osi_common_pb2 import Vector3d


sys.path.append("../..")

FRC = OSIRulesChecker()

PB_VECTOR3D = Vector3d()
PB_VECTOR3D.x = 1
PB_VECTOR3D.y = 2
VECTOR3D = LinkedProtoField(PB_VECTOR3D, "Vector3D")


class TestCheckIf(unittest.TestCase):
    """Test class of OSIDataContainer class"""

    def test_comply1(self):
        rule = Rule(verb="check_if", field_name='x',
                    params=[{'is_equal': 3, 'target': 'this.y'}],
                    extra_params={'do_check': [{'is_equal': 2}]})
        compliance = FRC.check_if(VECTOR3D, rule)
        self.assertTrue(compliance)

    def test_comply2(self):
        rule = Rule(verb="check_if", field_name='x',
                    params=[{'is_equal': 2, 'target': 'this.y'}],
                    extra_params={'do_check': [{'is_equal': 1}]})
        compliance = FRC.check_if(VECTOR3D, rule)
        self.assertTrue(compliance)

    def test_comply_is_set(self):
        rule = Rule(verb="check_if", field_name='x',
                    params=[{'is_equal': 2, 'target': 'this.y'}],
                    extra_params={'do_check': [{'is_set': None}]})
        compliance = FRC.check_if(VECTOR3D, rule)
        self.assertTrue(compliance)

    def test_not_comply(self):
        rule = Rule(verb="check_if", field_name='x',
                    params=[{'is_equal': 2, 'target': 'this.y'}],
                    extra_params={'do_check': [{'is_equal': 2}]})
        compliance = FRC.check_if(VECTOR3D, rule)
        self.assertFalse(compliance)

    def test_not_comply_is_set_if(self):
        rule = Rule(verb="check_if", field_name='z',
                    params=[{'is_equal': 2, 'target': 'this.y'}],
                    extra_params={'do_check': [{'is_set': None}]})
        compliance = FRC.check_if(VECTOR3D, rule)
        self.assertFalse(compliance)
