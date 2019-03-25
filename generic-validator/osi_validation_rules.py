import os
import copy
import yaml

from osi_rule_checker import OsiRuleChecker


class OsiValidationRules(OsiRuleChecker):
    """ This class collects validation rules """

    def from_yaml_directory(self, path):
        """ Collect validation rules found in the directory. """
        try:
            for filename in os.listdir(path):
                if filename.startswith('osi_') and filename.endswith(('.yml', '.yaml')):
                    self.from_yaml_file(os.path.join(path, filename))

        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

    def from_yaml_file(self, path):
        rules_file = open(path)
        self._rules.update(yaml.load(rules_file))

    def get_rules(self):
        return copy.deepcopy(self._rules)
