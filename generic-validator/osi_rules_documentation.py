from xml.dom import minidom

from osi_validation_rules import OSIValidationRules, MessageType, Field

class OSIRulesDocumentation:
    """This class creates a readable documentation from a set of rules. It is
    useful to create the KPIs documentation.
    """

    def __init__(self, ovr):
        self.rules = ovr.t_rules
        self.document = minidom.Document()

    def create_documentation(self):
        """Create the documentation
        """
        self.html_list = self.document.createElement('ul')
        self.scan_node(self.rules, 0)
        self.document.appendChild(self.html_list)

    def scan_node(self, node, deepness):
        """Scan recursively a node with a DFS style.
        """
        for key, value in node.nested_types.items():
            self.scan_node(value, deepness + 1)

        if isinstance(node, MessageType):
            for field, field_obj in node.fields.items():
                self.scan_field(field_obj)


    def scan_field(self, field):
        """Scan a list of rules
        """
        # for rule in field.rules:
        #     print(rule)
        print(field.message_path, field)
        list_element = self.document.createElement('li')
        link = self.document.createElement('a')
        link.setAttribute('href', '#')
        print(field.message_path.pretty_html())
        text = minidom.parseString('<span>' + field.message_path.pretty_html() + '</span>')._get_firstChild()
        link.appendChild(text)

        list_element.appendChild(link)
        self.html_list.appendChild(list_element)

if __name__ == "__main__":
    OVR = OSIValidationRules()
    OVR.from_yaml_directory('requirements-osi-3')
    DOC = OSIRulesDocumentation(OVR)

    DOC.create_documentation()
    print(DOC.document.toxml())
