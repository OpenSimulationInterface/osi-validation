import unittest
import osivalidator.osi_validation_rules as ovr

class TestValidationRules(unittest.TestCase):

    def test_creation_node(self):
        node = ovr.OSIRuleNode('foo', None)
        self.assertEqual(node.get_name(), 'foo')

    def test_add_type_from_path(self):
        container = ovr.TypeContainer()
        path = ['foo', 'bar', 'type']
        container.add_type_from_path(path)

        container.get_type(path)

if __name__ == '__main__':
    unittest.main()