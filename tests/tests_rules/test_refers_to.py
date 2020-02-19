"""Module for test class of OSIValidationRules class"""

import unittest

from osivalidator.osi_rules_checker import OSIRulesChecker
from osivalidator.linked_proto_field import LinkedProtoField
from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_groundtruth_pb2 import GroundTruth
from osivalidator.osi_rules import Rule, ProtoMessagePath, TypeRulesContainer


class TestRefersTo(unittest.TestCase):
    def setUp(self):
        self.FRC = OSIRulesChecker()

        sv1 = SensorView()
        linked_sv1 = LinkedProtoField(sv1, name="SensorView")

        gt1 = sv1.global_ground_truth
        linked_gt1 = LinkedProtoField(
            gt1, name="global_ground_truth", parent=linked_sv1
        )

        gt1.host_vehicle_id.value = 0
        hvid1 = gt1.host_vehicle_id
        self.linked_hvid1 = LinkedProtoField(
            hvid1, name="host_vehicle_id", parent=linked_gt1
        )

        sv2 = SensorView()
        linked_sv2 = LinkedProtoField(sv2, name="SensorView")

        gt2 = sv2.global_ground_truth
        linked_gt2 = LinkedProtoField(
            gt2, name="global_ground_truth", parent=linked_sv2
        )

        gt2.host_vehicle_id.value = 1
        hvid1 = gt2.host_vehicle_id
        self.linked_hvid2 = LinkedProtoField(
            hvid1, name="host_vehicle_id", parent=linked_gt2
        )

    def tearDown(self):
        del self.FRC
        del self.linked_hvid1
        del self.linked_hvid2

    def test_comply_refers_to(self):
        """
        Check if the message object is referenced correctly
        """
        container = TypeRulesContainer()
        proto_path = ProtoMessagePath(["GroundTruth", "host_vehicle_id", "refers_to"])
        container.add_type_from_path(proto_path)

        rule = Rule(
            verb="refers_to",
            params="MovingObject",
            extra_params=dict(),
            path=proto_path,
            field_name="host_vehicle_id",
        )
        rule.root = container
        self.FRC.refers_to(self.linked_hvid1, rule)
        self.FRC.refers_to(self.linked_hvid2, rule)
        self.FRC.refers_to(self.linked_hvid1, rule)

        references_list = self.FRC.id_manager._references

        print(references_list)

        # Check the instance type of the reference
        self.assertIsInstance(references_list[0][0], GroundTruth)

        # Check the id assignment of the reference to the object
        self.assertEqual(references_list[0][0].host_vehicle_id.value, 0)
        self.assertEqual(references_list[0][1], 0)
        self.assertEqual(references_list[0][2], "MovingObject")
