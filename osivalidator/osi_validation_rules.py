"""
This module contains all the useful classes to describe the tree of the
validation rules tree.
"""

import os
from copy import deepcopy
from enum import Enum
import yaml


class OSIValidationRules:
    """ This class collects validation rules """

    def __init__(self):
        self.rules = dict()
        self.t_rules = TypeContainer()

    def from_yaml_directory(self, path):
        """ Collect validation rules found in the directory. """
        try:
            for filename in os.listdir(path):
                if filename.startswith('osi_') and filename.endswith(('.yml',
                                                                      '.yaml')):
                    self.from_yaml_file(os.path.join(path, filename))

        except FileNotFoundError:
            print('Error while reading files OSI-rules. Exiting!')

        translate_rules(self.rules, self.t_rules)

    def from_yaml_file(self, path):
        """Import from a file
        """
        rules_file = open(path)
        self.rules.update(yaml.load(rules_file, Loader=yaml.SafeLoader))

    def get_rules(self):
        """Return the rules
        """
        return deepcopy(self.rules)


class ProtoMessagePath:
    """Represents a path to a message object"""

    def __init__(self, inheritance=None):
        self.inheritance = inheritance or []

    def __repr__(self):
        return ".".join(self.inheritance)

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

    def __init__(self, name, message_path):
        self.name = name
        self.message_path = message_path

    def get_name(self):
        """Return the name of the node"""
        return self.name

    def get_path(self):
        """Return the path of the node"""
        return self.message_path


class TypeContainer(OSIRuleNode):
    """This class defines either a MessageType or a list of MessageTypes"""

    def __init__(self, name=None, path=None):
        super().__init__(name, path or ProtoMessagePath())
        self.nested_types = dict()

    def add_type(self, name, fields=None):
        """Add a message type in the TypeContainer"""
        new_message_t = MessageType(name, fields,
                                    self.message_path.child_path(name))
        self.nested_types[name] = new_message_t
        return new_message_t


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
        new_message_t = MessageType(name, fields, ProtoMessagePath(path))

        child = self
        for node in path[:-1]:
            try:
                child = child.nested_types[node]
            except KeyError:
                child = child.add_type(node)

        child.nested_types[path[-1]] = new_message_t


        return new_message_t


    def get_type(self, message_path):
        """Get a MessageType by name or path"""
        if isinstance(message_path, list):
            message_t = self
            for i in message_path:
                message_t = message_t.nested_types[i]
            return message_t
        if isinstance(message_path, str):
            return self.nested_types[message_path]

        raise TypeError('parameter must be list or str')

    def __getitem__(self, name):
        return self.nested_types[name]

    def __repr__(self):
        return f'TypeContainer({len(self.nested_types)}):\n' + \
               '\n'.join(map(str, self.nested_types))


class MessageType(TypeContainer):
    """This class manages the fields of a Message Type"""

    def __init__(self, name, fields, path):
        super().__init__(name, path)
        self.fields = dict()
        if fields is not None:
            translate_rules(fields, self)

    def add_field(self, field_name, rules=None):
        """Add a field with or without rules to a Message Type"""
        self.fields[field_name] = \
            Field(field_name, self.message_path.child_path(field_name), rules)

    def get_field(self, field_name):
        return self.fields[field_name]

    def __repr__(self):
        return f'MessageType({len(self.fields)}): {self.fields}\n' + \
            f'Nested types ({len(self.nested_types)})' + \
            (': ' + ', '.join(self.nested_types.keys()) if self.nested_types \
                else '')


class Field(OSIRuleNode):
    """This class manages the rules of a Message Type"""

    def __init__(self, name, path, rules=None):
        super().__init__(name, path)
        self.rules = dict()
        self.must_be_set = False
        self.must_be_set_if = None

        if rules is not None and isinstance(rules, list):
            for rule in rules:
                self.add_rule(rule)

    def add_rule(self, rule):
        """Add a new rule to a field"""
        if isinstance(rule, dict):
            verb, params = next(iter(rule.items()))
        else:
            verb = rule
            params = None

        new_rule = Rule(verb, self.message_path.child_path(verb), params)
        self.rules[new_rule.verb] = new_rule

        if new_rule.verb == "is_set":
            self.must_be_set = True
        elif new_rule.verb == "is_set_if":
            self.must_be_set_if = params

    def __getitem__(self, rule_verb):
        return self.rules[rule_verb]

    def __repr__(self):
        return f"Field({len(self.rules)}):{[self.rules[r] for r in self.rules]}"


class Rule(OSIRuleNode):
    """This class manages one rule"""

    def __init__(self, verb, path, params=None, severity=None):
        super().__init__(verb, path)
        self.construct(verb, params, severity)

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


class Severity(Enum):
    """Descript the severity of the raised error if a rule does not comply."""
    WARN = "warning"
    ERROR = "error"


def translate_rules(rules, t_rules):
    """Translate dict rules into objects rules"""

    for key, value in rules.items():
        is_message_type = key[0].isupper()

        if is_message_type and isinstance(value, dict):
            new_message_t = t_rules.add_type(key)
            translate_rules(value, new_message_t)
        elif isinstance(value, list):
            t_rules.add_field(key, value)
        elif value is not None:
            raise TypeError(
                'only dict and list are accepted, parsing problem.')


if __name__ == "__main__":
    OVR = OSIValidationRules()
    OVR.from_yaml_directory('requirements-osi-3')

    # T_RULES = TypeContainer()
    # translate_rules(OVR.rules, T_RULES)

    print(OVR.t_rules)
    print(OVR.t_rules.get_type(['LaneBoundary', 'BoundaryPoint']))
    print(OVR.t_rules['LaneBoundary'])
