"""Module for test class of OSIValidationRules class"""

import unittest

from osi3.osi_sensorview_pb2 import SensorView

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule, TypeRulesContainer, ProtoMessagePath


class TestFirstElement(unittest.TestCase):
    def setUp(self):
        self.FRC = OSIRulesChecker()

        sv1 = SensorView()
        linked_sv1 = LinkedProtoField(sv1, name="SensorView")
        gt1 = sv1.global_ground_truth
        linked_gt1 = LinkedProtoField(
            gt1, name="global_ground_truth", parent=linked_sv1
        )

        gtlb1 = gt1.lane_boundary.add()
        linked_gtlb1 = LinkedProtoField(gtlb1, name="lane_boundary", parent=linked_gt1)

        bladd1 = gtlb1.boundary_line.add()
        bladd1.position.x = 1699.2042678176733
        bladd1.position.y = 100.16895580204906
        bladd1.position.z = 0.0
        bladd1.width = 0.13
        bladd1.height = 0.0

        self.lb1 = LinkedProtoField(bladd1, name="boundary_line", parent=linked_gtlb1)
        self.lb1.path = "SensorView.global_ground_truth.lane_boundary.boundary_line"
        # self.lb1.parent =

        sv2 = SensorView()
        linked_sv2 = LinkedProtoField(sv2, name="SensorView")

        gt2 = sv2.global_ground_truth
        linked_gt2 = LinkedProtoField(
            gt2, name="global_ground_truth", parent=linked_sv2
        )

        gtlb2 = gt2.lane_boundary.add()
        linked_gtlb2 = LinkedProtoField(gtlb2, name="lane_boundary", parent=linked_gt2)

        bladd2 = gtlb2.boundary_line.add()
        bladd2.position.x = 1699.2042678176733
        bladd2.position.y = 100.16895580204906
        bladd2.position.z = 0.0
        bladd2.width = 0.14
        bladd2.height = 0.13
        self.lb2 = LinkedProtoField(bladd2, name="boundary_line", parent=linked_gtlb2)
        self.lb2.path = "SensorView.global_ground_truth.lane_boundary.boundary_line"

    def tearDown(self):
        del self.FRC

    def test_comply_first_element(self):
        field_list = [self.lb1, self.lb2]
        container = TypeRulesContainer()
        proto_path = ProtoMessagePath(["LaneBoundary", "BoundaryPoint"])
        container.add_type_from_path(proto_path)
        container.add_type_from_path(ProtoMessagePath(["Vector3d"]))

        rule = Rule(
            verb="first_element",
            params={"width": [{"is_equal_to": 0.13}], "height": [{"is_equal_to": 0.0}]},
            path=proto_path,
            extra_params=dict(),
            field_name="boundary_line",
        )
        rule.root = container
        compliance = self.FRC.first_element(field_list, rule)
        self.assertTrue(compliance)

    def test_not_comply_first_element(self):
        field_list = [self.lb1, self.lb2]
        container = TypeRulesContainer()
        proto_path = ProtoMessagePath(["LaneBoundary", "BoundaryPoint"])
        container.add_type_from_path(proto_path)
        container.add_type_from_path(ProtoMessagePath(["Vector3d"]))

        rule = Rule(
            verb="first_element",
            params={
                "width": [{"is_equal_to": 0.11}],
                "height": [{"is_equal_to": 0.13}],
            },
            path=proto_path,
            extra_params=dict(),
            field_name="boundary_line",
        )
        rule.root = container
        compliance = self.FRC.first_element(field_list, rule)
        self.assertFalse(compliance)
