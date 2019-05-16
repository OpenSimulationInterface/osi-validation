"""
This module intends to handle tools to generate KPI documentation from the YAML
definition files.
"""

from xml.dom import minidom

from .osi_validation_rules import OSIValidationRules, MessageType


class OSIRulesDocumentation:
    """This class creates a readable documentation from a set of rules. It is
    useful to create the KPIs documentation.
    """

    def __init__(self, ovr):
        self.rules = ovr.t_rules
        self.document = minidom.Document()
        self.html_list = self.document.createElement('ul')
        self.html_list.setAttribute('id', 'myUL')

    def create_documentation(self):
        """Create the documentation
        """
        self.scan_node(self.rules, 0)
        self.document.appendChild(self.html_list)

    def scan_node(self, node, deepness):
        """Scan recursively a node with a DFS style.
        """
        for _key, value in node.nested_types.items():
            self.scan_node(value, deepness + 1)

        if isinstance(node, MessageType):
            for _field, field_obj in node.fields.items():
                self.scan_field(field_obj)

    def scan_field(self, field):
        """Scan a list of rules
        """
        list_element = self.document.createElement('li')
        link = self.document.createElement('a')
        link.setAttribute('href', '#')
        text = minidom.parseString(
            '<span>' + field.message_path.pretty_html() + '</span>').firstChild
        link.appendChild(text)

        list_element.appendChild(link)
        self.html_list.appendChild(list_element)


if __name__ == "__main__":
    OVR = OSIValidationRules()
    OVR.from_yaml_directory('requirements-osi-3')
    DOC = OSIRulesDocumentation(OVR)

    DOC.create_documentation()
    print(DOC.document.toxml())
