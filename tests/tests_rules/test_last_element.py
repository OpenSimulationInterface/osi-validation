"""Module for test class of OSIValidationRules class"""

import sys
import unittest

from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_lane_pb2 import LaneBoundary

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule, TypeRulesContainer, MessageTypeRules

sys.path.append("../..")


class TestFirstElement(unittest.TestCase):

    def setUp(self):
        self.FRC = OSIRulesChecker()

        gt1 = GroundTruth()
        gtlb1 = gt1.lane_boundary.add()
        bladd1 = gtlb1.boundary_line.add()
        bladd1.position.x = 1699.2042678176733
        bladd1.position.y = 100.16895580204906
        bladd1.position.z = 0.0
        bladd1.width = 0.13
        bladd1.height = 0.0
        self.lb1 = LinkedProtoField(bladd1, "GroundTruth")

        gt2 = GroundTruth()
        gtlb2 = gt2.lane_boundary.add()
        bladd2 = gtlb2.boundary_line.add()
        bladd2.position.x = 1699.2042678176733
        bladd2.position.y = 100.16895580204906
        bladd2.position.z = 0.0
        bladd2.width = 0.13
        bladd2.height = 0.0
        self.lb2 = LinkedProtoField(bladd2, "GroundTruth")

    def tearDown(self):
        del self.FRC

    # TODO In progress
    def test_comply_last_element(self):
        field_list = [self.lb1, self.lb2]

        trc = TypeRulesContainer().add_type(MessageTypeRules(name='LaneBoundary'))
        trc.add_type(MessageTypeRules(name='BoundaryPoint'))

        rule = trc.add_rule(Rule(verb="last_element",
                                 params=[{'is_equal': 0.13, 'target': "this.height"}],
                                 field_name='boundary_line'))

        compliance = self.FRC.last_element(field_list, rule)

        print(compliance)
