"""Module for test class of OSIValidationRules class"""

import unittest
from osivalidator.osi_rules_checker import OSIRulesChecker
from osi3.osi_sensorview_pb2 import SensorView
from osivalidator.linked_proto_field import LinkedProtoField
from osivalidator.osi_rules import Rule, TypeRulesContainer, ProtoMessagePath


class TestIsGlobalUnique(unittest.TestCase):
    def setUp(self):
        self.FRC = OSIRulesChecker()

        sv = SensorView()
        linked_sv = LinkedProtoField(sv, name="SensorView")
        sid = sv.sensor_id
        sid.value = 0
        self.linked_sid = LinkedProtoField(sid, name="sensor_id", parent=linked_sv)

        sv2 = SensorView()
        linked_sv2 = LinkedProtoField(sv2, name="SensorView")
        sid2 = sv2.sensor_id
        sid2.value = 2
        self.linked_sid2 = LinkedProtoField(sid2, name="sensor_id", parent=linked_sv2)

    def tearDown(self):
        del self.FRC
        del self.linked_sid
        del self.linked_sid2

    def test_comply_is_globally_unique(self):
        """
        Test if the ID Manager has unique indices
        """
        container = TypeRulesContainer()
        proto_path = ProtoMessagePath(["SensorView", "sensor_id", "is_globally_unique"])
        container.add_type_from_path(proto_path)

        rule = Rule(
            verb="is_globally_unique",
            field_name="sensor_id",
            extra_params=dict(),
            path=proto_path,
        )
        rule.root = container
        self.FRC.is_globally_unique(self.linked_sid, rule)
        self.FRC.is_globally_unique(self.linked_sid2, rule)
        self.FRC.is_globally_unique(self.linked_sid2, rule)
        index_dict = self.FRC.id_manager._index
        self.assertEqual(2, len(index_dict))
