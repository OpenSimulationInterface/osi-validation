"""Module for test class of OSIValidationRules class"""

import unittest
from osivalidator.osi_rules import (
    Rule,
    TypeRulesContainer,
    ProtoMessagePath,
    OSIRules,
    OSIRuleNode,
)


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


if __name__ == "__main__":
    unittest.main()
