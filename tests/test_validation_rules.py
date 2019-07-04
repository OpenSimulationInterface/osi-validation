"""Module for test class of OSIValidationRules class"""

import sys
import unittest
from osivalidator import osi_rules

sys.path.append("..")


class TestValidationRules(unittest.TestCase):

    """Test class for OSIValidationRules class"""

    def test_from_directory(self):
        """Test import from directory"""
        ovr = osi_rules.OSIRules()
        ovr.from_yaml_directory('requirements-osi-3')
        test_path = osi_rules.ProtoMessagePath(
            ['LaneBoundary', 'BoundaryPoint'])
        ovr.t_rules.get_type(test_path)

    def test_creation_node(self):
        """Test creation of a node in OSI rules"""
        node = osi_rules.OSIRuleNode('foo', None)
        self.assertEqual(node.get_name(), 'foo')

    def test_add_type_from_path(self):
        """Test the adding of a Message type from a path in the rule tree"""
        container = osi_rules.TypeContainer()
        path = osi_rules.ProtoMessagePath(['foo', 'bar', 'type'])
        container.add_type_from_path(path)
        container.get_type(path)

    def test_parse_yaml(self):
        """ Test the YAML parsing"""
        raw = """HostVehicleData:
  location:
    is_set:
  location_rmse:
    is_set:"""
        validation_rules = osi_rules.OSIRules()
        validation_rules.from_yaml(raw, only=True)
        rules = validation_rules.t_rules
        field = rules['HostVehicleData'].get_field('location')
        rule_check = osi_rules.Rule('is_set')
        rule_check.path = osi_rules.ProtoMessagePath(
            ["HostVehicleData", "location.is_set"])
        self.assertEqual(field['is_set'], rule_check)


if __name__ == '__main__':
    unittest.main()
