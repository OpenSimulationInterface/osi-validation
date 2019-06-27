import unittest
import osivalidator.osi_rules as ovr
import os


class TestValidationRules(unittest.TestCase):

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def test_from_directory(self):
        OVR = ovr.OSIRules()
        OVR.from_yaml_directory(
            os.path.join(self.dir_path, 'osivalidator/requirements-osi-3'))
        OVR.t_rules.get_type(['LaneBoundary', 'BoundaryPoint'])

    def test_creation_node(self):
        node = ovr.OSIRuleNode('foo', None)
        self.assertEqual(node.get_name(), 'foo')

    def test_add_type_from_path(self):
        container = ovr.TypeContainer()
        path = ovr.ProtoMessagePath(['foo', 'bar', 'type'])
        container.add_type_from_path(path)
        container.get_type(path)

    def test_parse_yaml(self):
        raw = """HostVehicleData:
  location:
    is_set:
  location_rmse:
    is_set:"""
        validation_rules = ovr.OSIRules()
        validation_rules.from_yaml(raw, only=True)
        rules = validation_rules.t_rules
        field = rules['HostVehicleData'].get_field('location')
        rule_check = ovr.Rule('is_set')
        rule_check.path = ovr.ProtoMessagePath(
            ["HostVehicleData", "location.is_set"])
        self.assertEqual(field['is_set'], rule_check)


if __name__ == '__main__':
    unittest.main()
