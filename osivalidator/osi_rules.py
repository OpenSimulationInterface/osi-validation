"""
This module contains all the useful classes to describe the tree of the
validation rules tree.
"""

import os
from copy import deepcopy
from enum import Enum

import ruamel.yaml as yaml

from .osi_doxygen_xml import OSIDoxygenXML


class OSIRules:
    """ This class collects validation rules """

    def __init__(self):
        self.rules = dict()
        self.t_rules = TypeContainer()

    def from_yaml_directory(self, path=None):
        """ Collect validation rules found in the directory. """

        if not path:
            dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir_path, 'requirements-osi-3')

        exts = ('.yml', '.yaml')
        try:
            for filename in os.listdir(path):
                if filename.startswith('osi_') and filename.endswith(exts):
                    self.from_yaml_file(os.path.join(path, filename), False)

        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

        self.translate_rules()

    def from_yaml_file(self, path, only=True):
        """Import from a file
        """
        rules_file = open(path)
        self.rules.update(yaml.load(rules_file, Loader=yaml.SafeLoader))
        rules_file.close()

        if only:
            self.translate_rules()

    def from_yaml(self, yaml_content, only=True):
        """Import from a string
        """
        self.rules.update(yaml.load(yaml_content, Loader=yaml.SafeLoader))

        if only:
            self.translate_rules()

    def from_xml_doxygen(self):
        """Parse the Doxygen XML documentation to get the rules
        """
        dox_xml = OSIDoxygenXML()
        dox_xml.generate_osi_doxygen_xml()
        rules = dox_xml.parse_rules()

        for field_rules_tuple in rules:
            message_t_path = field_rules_tuple[0][:-1]
            field_name = field_rules_tuple[0][-1]
            field_rules = field_rules_tuple[1]

            message_t = self.t_rules.add_type_from_path(message_t_path)
            for field_rule in field_rules:
                message_t.add_field(Field(field_name, field_rule))

    def get_rules(self):
        """Return the rules
        """
        return deepcopy(self.rules)

    def translate_rules(self, rules=None, t_rules=None):
        """Translate dict rules into objects rules"""

        if rules is None:
            rules = self.rules
        if t_rules is None:
            t_rules = self.t_rules

        for key, value in rules.items():
            is_message_type = key[0].isupper()

            if is_message_type and isinstance(value, dict):
                new_message_t = t_rules.add_type(MessageType(key))
                self.translate_rules(value, new_message_t)
            elif isinstance(value, list):
                field = t_rules.add_field(Field(key))
                for yaml_rule in value:
                    if isinstance(yaml_rule, str):
                        field.add_rule(Rule(yaml_rule))
                    elif isinstance(yaml_rule, dict):
                        (verb, params), = yaml_rule.items()
                        field.add_rule(Rule(verb, params))
            elif isinstance(value, dict):
                field = t_rules.add_field(Field(key))
                for verb, params in value.items():
                    field.add_rule(Rule(verb, params))

            elif value is not None:
                raise TypeError(
                    f'must be dict or list, got {type(rules).__name__}')


class ProtoMessagePath:
    """Represents a path to a message object"""

    def __init__(self, inheritance=None):
        self.inheritance = inheritance or []

    def __repr__(self):
        return ".".join(self.inheritance)

    def __getitem__(self, parent):
        return self.inheritance[parent]

    def pretty_html(self):
        """Return a pretty html version of the message path"""
        return ".".join(map(lambda l: "<b>"+l+"</b>", self.inheritance[:-1])) \
            + "." + self.inheritance[-1]

    def child_path(self, child_name):
        """Return a new path for the child of the message named child_name"""
        new_path = deepcopy(self)
        new_path.inheritance.append(child_name)

        return new_path


class OSIRuleNode:
    """Represents any node in the tree of OSI rules"""

    def __init__(self, name, message_path=None):
        self.name = name
        self.path = message_path

    def get_name(self):
        """Return the name of the node"""
        return self.name

    def get_path(self):
        """Return the path of the node"""
        return self.path


class TypeContainer(OSIRuleNode):
    """This class defines either a MessageType or a list of MessageTypes"""

    def __init__(self, name="", nested_types=None):
        super().__init__(name, ProtoMessagePath())
        self.nested_types = nested_types or dict()

    def add_type(self, message_type):
        """Add a message type in the TypeContainer"""
        message_type = deepcopy(message_type)
        message_type.path = self.path.child_path(message_type.name)
        self.nested_types[message_type.name] = message_type
        return message_type

    def add_type_from_path(self, path, fields=None):
        """Add a message type in the TypeContainer by giving a path

        The path must be a list and the last element of the list is the name of
        the message type.

        If the message type already exists, it is not added.
        """

        try:
            return self.get_type(path)
        except KeyError:
            pass

        name = path[-1]
        new_message_t = MessageType(name, fields)

        new_message_t.path = path

        child = self
        for node in path.inheritance[:-1]:
            try:
                child = child.nested_types[node]
            except KeyError:
                child = child.add_type(MessageType(node))

        child.nested_types[path.inheritance[-1]] = new_message_t

        return new_message_t

    def get_type(self, message_path):
        """Get a MessageType by name or path"""
        if isinstance(message_path, ProtoMessagePath):
            message_t = self
            for i in message_path.inheritance:
                message_t = message_t.nested_types[i]
            return message_t
        if isinstance(message_path, str):
            return self.nested_types[message_path]

        raise TypeError('parameter must be ProtoMessagePath or str')

    def __getitem__(self, name):
        return self.nested_types[name]

    def __repr__(self):
        return f'TypeContainer({len(self.nested_types)}):\n' + \
               '\n'.join(map(str, self.nested_types))


class MessageType(TypeContainer):
    """This class manages the fields of a Message Type"""

    def __init__(self, name, fields=None):
        super().__init__(name)
        self.fields = dict()
        if isinstance(fields, list):
            for field in fields:
                self.fields[field.name] = field
        elif isinstance(fields, dict):
            self.fields = fields

    def add_field(self, field):
        """Add a field with or without rules to a Message Type"""
        field = deepcopy(field)
        field.path = self.path.child_path(field.name)
        self.fields[field.name] = field
        return field

    def get_field(self, field_name):
        return self.fields[field_name]

    def __getitem__(self, field_name):
        return self.get_field(field_name)

    def __repr__(self):
        return f'MessageType({len(self.fields)}): {self.fields}\n' + \
            f'Nested types ({len(self.nested_types)})' + \
            (': ' + ', '.join(self.nested_types.keys()) if self.nested_types
             else '')


class Field(OSIRuleNode):
    """This class manages the rules of a Message Type"""

    def __init__(self, name, rules=None):
        super().__init__(name)
        self.rules = dict()

        if isinstance(rules, list):
            for rule in rules:
                self.add_rule(rule)

    def add_rule(self, rule):
        """Add a new rule of verb rule to a field with the parameters params.
        rule can also be a dictionary containing one key (the verb) with one
        value (the parameters).
        """
        rule = deepcopy(rule)
        rule.path = self.path.child_path(rule.name)
        self.rules[rule.verb] = rule

    def has_rule(self, rule):
        """Check if a field has the rule `rule`"""
        return rule in self.rules

    def __getitem__(self, rule_verb):
        return self.rules[rule_verb]

    def __repr__(self):
        nested_rules = [self.rules[r] for r in self.rules]
        return f"Field({len(self.rules)}):{nested_rules}"


class Rule(OSIRuleNode):
    """This class manages one rule"""

    def __init__(self, verb, params=None, severity=None):
        super().__init__(verb)
        self.construct(verb, params, severity)
        self.field_name = self.path[-2]

    def construct(self, verb, params, severity=None):
        """Construct an empty rule"""
        self.params = params

        if verb[-1] == "!" or severity == Severity.ERROR:
            self.severity = Severity.ERROR
            verb = verb[:-1]
        else:
            self.severity = Severity.WARN

        self.verb = verb

    def __repr__(self):
        return f'{self.verb}' + (f"({self.params})" or "")

    def __eq__(self, other):
        return self.verb == other.verb and self.params == other.params \
            and self.severity == other.severity


class Severity(Enum):
    """Descript the severity of the raised error if a rule does not comply."""
    WARN = "warning"
    ERROR = "error"
