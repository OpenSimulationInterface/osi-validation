from osi_validation_rules import OSIValidationRules

class OSIRulesDocumentation:
    """This class creates a readable documentation from a set of rules. It is
    useful to create the KPIs documentation.
    """

    def __init__(self, ovr):
        self.rules = ovr.rules

    def create_documentation(self):
        """Create the documentation
        """
        scan_node(self.rules, 0)

def scan_node(node, deepness):
    """Scan recursively a node with a DFS style.
    """
    for key, value in node.items():
        is_message_type = key[0].isupper()
        print(deepness, key, is_message_type)

        if is_message_type and isinstance(value, dict):
            scan_node(value, deepness + 1)
        elif isinstance(value, list):
            scan_rules(value)


def scan_rules(rules):
    """Scan a list of rules
    """
    for rule in rules:
        if isinstance(rule, dict):
            key = next(iter(rule))
            print("-", key, ":", rule[key])
        else:
            print("-", rule)

if __name__ == "__main__":
    OVR = OSIValidationRules()
    OVR.from_yaml_directory('requirements-osi-3')
    DOC = OSIRulesDocumentation(OVR)

    DOC.create_documentation()
