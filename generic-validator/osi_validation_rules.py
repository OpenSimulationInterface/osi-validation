import os
import copy
import yaml


class OSIValidationRules:
    """ This class collects validation rules """

    def __init__(self):
        self.rules = dict()

    def from_yaml_directory(self, path):
        """ Collect validation rules found in the directory. """
        try:
            for filename in os.listdir(path):
                if filename.startswith('osi_') and filename.endswith(('.yml', '.yaml')):
                    self.from_yaml_file(os.path.join(path, filename))

        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

    def from_yaml_file(self, path):
        """Import from a file
        """
        rules_file = open(path)
        self.rules.update(yaml.load(rules_file))

    def get_rules(self):
        """Return the rules
        """
        return copy.deepcopy(self.rules)
