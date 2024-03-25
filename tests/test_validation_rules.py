"""Module for test class of OSIValidationRules class"""

import unittest
from glob import *
import os
import shutil
import yamale
from osivalidator.osi_rules import (
    Rule,
    TypeRulesContainer,
    ProtoMessagePath,
    OSIRules,
    OSIRuleNode,
)
from rules2yml import gen_yml_rules


class TestValidationRules(unittest.TestCase):

    """Test class for OSIValidationRules class"""

    def test_from_directory(self):
        """Test import from directory"""
        ovr = OSIRules()
        ovr.from_yaml_directory("rules")
        test_path = ProtoMessagePath(["LaneBoundary", "BoundaryPoint"])
        ovr_container = ovr.rules.get_type(test_path)
        self.assertIsInstance(ovr_container.path, ProtoMessagePath)
        self.assertEqual(test_path.path, ovr_container.path.path)

    def test_creation_node(self):
        """Test creation of a node in OSI rules"""
        node = OSIRuleNode("foo")
        self.assertEqual(node.path, "foo")

    def test_add_type_from_path(self):
        """Test the adding of a Message type from a path in the rule tree"""
        container = TypeRulesContainer()
        path = ProtoMessagePath(["foo", "bar", "type"])
        container.add_type_from_path(path)
        typecontainer = container.get_type(path)
        self.assertIsInstance(typecontainer.path, ProtoMessagePath)
        self.assertEqual(path.path, typecontainer.path.path)

    def test_parse_yaml(self):
        """Test the YAML parsing"""
        raw = """
        HostVehicleData:
            location:
                - is_set:
            location_rmse:
                - is_set: 
        """
        validation_rules = OSIRules()
        validation_rules.from_yaml(raw)
        rules = validation_rules.rules
        field = rules["HostVehicleData"].get_field("location")
        rule_check = Rule(
            verb="is_set",
            field_name="location",
            path=ProtoMessagePath(["HostVehicleData", "location", "is_set"]),
        )

        self.assertEqual(field["is_set"], rule_check)

    def test_yaml_generation(self):
        gen_yml_rules("unit_test_rules/")

        num_proto_files = len(glob("open-simulation-interface/*.proto"))
        num_rule_files = len(glob("unit_test_rules/*.yml"))
        num_rule_schema_files = len(glob("unit_test_rules/schema/*.yml"))
        self.assertEqual(num_proto_files, num_rule_files)
        self.assertEqual(num_rule_files, num_rule_schema_files)

        # clean up
        if os.path.isdir("unit_test_rules"):
            shutil.rmtree("unit_test_rules")

    def test_yaml_schema_fail(self):
        gen_yml_rules("unit_test_rules/")

        # alter exemplary rule for fail check
        raw_sensorspecific = """RadarSpecificObjectData:
  rcs:
LidarSpecificObjectData:
  maximum_measurement_distance_sensor:
    - is_greater_than_or_equal_to: 0
  probability:
    - is_less_than_or_equal_to: x
    - is_greater_than_or_equal_to: 0
  trilateration_status:
  trend:
  signalway:
  Signalway:
    sender_id:
    receiver_id:
"""

        os.remove("unit_test_rules/osi_sensorspecific.yml")
        with open("unit_test_rules/osi_sensorspecific.yml", "w") as rule_file:
            rule_file.write(raw_sensorspecific)

        validation_rules = OSIRules()
        with self.assertRaises(yamale.yamale_error.YamaleError):
            validation_rules.validate_rules_yml(
                "unit_test_rules/osi_sensorspecific.yml"
            )

        # clean up
        if os.path.isdir("unit_test_rules"):
            shutil.rmtree("unit_test_rules")


if __name__ == "__main__":
    unittest.main()
