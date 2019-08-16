"""
This module carry the XML version of Doxygen documentation to parse the rules
into it.
"""

import os
import glob

import ruamel.yaml as yaml
import defusedxml.ElementTree as ET

from doxygen import ConfigParser
from doxygen import Generator


class OSIDoxygenXML:
    """
    This class creates XML from \*.proto Files Documentation of OSI and can parse the rules from it.
    """

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        osivalidator_path = os.path.dirname(dir_path)
        self.osi_path = os.path.join(
            osivalidator_path, 'open-simulation-interface')
        self.osi_doc_path = os.path.join(self.osi_path, 'doc')

        proto2cpp_path = os.path.join(osivalidator_path, 'proto2cpp')
        self.proto2cpp_file_path = os.path.join(proto2cpp_path, "proto2cpp.py")

    def generate_osi_doxygen_xml(self):
        """
        Generate the Doxygen XML documentation in the OSI path
        """

        configuration = f'''
        PROJECT_NAME           = osi-validation
        INPUT                  = {self.osi_path}
        OUTPUT_DIRECTORY       = {self.osi_doc_path}
        EXTENSION_MAPPING      = proto=C++
        FILE_PATTERNS          = *.proto
        INPUT_FILTER           = "python {self.proto2cpp_file_path}"
        GENERATE_XML           = YES
        GENERATE_HTML          = YES
        GENERATE_LATEX         = NO
        XML_PROGRAMLISTING     = NO
        ALIASES                = rules="<pre class=\"rules\">"
        ALIASES               += endrules="</pre>"
        '''

        doxyfile_path = os.path.join(self.osi_path, 'Doxyfile_validation')
        doxyfile = open(doxyfile_path, 'w')
        doxyfile.write(configuration)
        doxyfile.close()

        config_parser = ConfigParser()
        config_parser.load_configuration(doxyfile_path)

        doxy_builder = Generator(doxyfile_path)
        doxy_builder.build(clean=False, generate_zip=False)

    def get_files(self):
        """
        Return the path of the fields in OSI
        """
        return glob.glob(os.path.join(self.osi_path, 'doc', 'xml', '*.xml'))

    def parse_rules(self):
        """
        Parse the Doxygen XML documentation to get the rules
        """
        xml_files = self.get_files()

        rules = list()

        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            memberdefs = tree.findall(
                "./compounddef/sectiondef/memberdef[@kind='variable']")
            for memberdef in memberdefs:
                attr_path = memberdef.findtext(
                    'definition').split()[-1].split('::')
                if attr_path[0] != 'osi3':
                    continue
                attr_path.pop(0)
                attr_rule = memberdef.findtext(
                    './detaileddescription//preformatted[last()]')
                if not attr_rule:
                    continue

                rules_lines = attr_rule.split('\n')

                for line_no, line in enumerate(rules_lines):
                    if line.find(":") == -1 and line:
                        rules_lines[line_no] += ":"

                attr_rule = "\n".join(rules_lines)

                try:
                    dict_rules = yaml.safe_load(attr_rule)
                except (yaml.parser.ParserError,
                        yaml.parser.ScannerError) as error:
                    print(attr_path, attr_rule, error)
                else:
                    rules.append((attr_path, dict_rules))
        return rules


if __name__ == '__main__':
    osidx = OSIDoxygenXML()
    osidx.generate_osi_doxygen_xml()
