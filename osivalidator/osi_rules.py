"""
This module contains all the useful classes to describe the tree of the
validation rules tree.
"""

import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from copy import deepcopy
from enum import Enum

from ruamel.yaml import YAML
from pathlib import Path

import osi_rules_implementations


class OSIRules:
    """This class collects validation rules"""

    def __init__(self):
        self.rules = TypeRulesContainer()
        self.nested_fields = {
            "dimension",
            "position",
            "velocity",
            "acceleration",
            "orientation",
            "orientation_rate",
            "orientation_acceleration",
        }

    def from_yaml_directory(self, path=None):
        """Collect validation rules found in the directory."""

        if not path:
            dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir_path, "rules")

        exts = (".yml", ".yaml")
        try:
            for filename in os.listdir(path):
                if filename.startswith("osi_") and filename.endswith(exts):
                    self.from_yaml_file(os.path.join(path, filename))

        except FileNotFoundError:
            print("Error while reading files OSI-rules. Exiting!")

    def from_yaml_file(self, path):
        """Import from a file"""
        yaml = YAML(typ="safe")
        self.from_dict(rules_dict=yaml.load(Path(path)))

    def from_yaml(self, yaml_content):
        """Import from a string"""
        yaml = YAML(typ="safe")
        self.from_dict(rules_dict=yaml.load(yaml_content))

    def get_rules(self):
        """Return the rules"""
        return self.rules

    def from_dict(self, rules_dict=None, rules_container=None):
        """Translate dict rules into objects rules"""

        rules_container = rules_container or self.rules

        for key, value in rules_dict.items():
            if key[0].isupper() and isinstance(value, dict):  # it's a nested type
                new_message_t = rules_container.add_type(MessageTypeRules(name=key))
                if value is not None:
                    self.from_dict(value, new_message_t)

            elif key in self.nested_fields and isinstance(value, dict):
                new_message_t = rules_container.add_type(
                    MessageTypeRules(name=key),
                    path=f"{rules_container.type_name}.{key}",
                )
                if value is not None:
                    self.from_dict(value, new_message_t)

            elif isinstance(value, list):  # it's a field
                field = rules_container.add_field(FieldRules(name=key))
                for rule_dict in value:  # iterate over rules
                    field.add_rule(Rule(dictionary=rule_dict))

            elif value is not None:
                sys.stderr.write(
                    "must be dict or list, got " + type(rules_dict).__name__ + "\n"
                )


class ProtoMessagePath:
    """Represents a path to a message object"""

    def __init__(self, path=None):
        if path and not all(isinstance(component, str) for component in path):
            sys.stderr.write("Path must be str list, found " + str(path) + "\n")
        self.path = deepcopy(path) or []

    def __repr__(self):
        return ".".join(self.path)

    def __getitem__(self, parent):
        return self.path[parent]

    def pretty_html(self):
        """Return a pretty html version of the message path"""
        return (
            ".".join(map(lambda l: "<b>" + l + "</b>", self.path[:-1]))
            + "."
            + self.path[-1]
        )

    def child_path(self, child):
        """Return a new path for the child"""
        new_path = deepcopy(self)
        new_path.path.append(child)

        return new_path


class OSIRuleNode:
    """Represents any node in the tree of OSI rules"""

    def __init__(self, path=None):
        self._path = path
        self.root = None

    @property
    def path(self):
        """Return the path of the node"""
        return self._path

    @path.setter
    def path(self, path):
        new_path = ProtoMessagePath(path=path.path)
        self._path = new_path


class TypeRulesContainer(OSIRuleNode):
    """This class defines either a MessageType or a list of MessageTypes"""

    def __init__(self, nested_types=None, root=None):
        super().__init__(path=ProtoMessagePath())
        self.nested_types = nested_types or dict()
        self.root = root if root else self

    def add_type(self, message_type, path=None):
        """Add a message type in the TypeContainer"""
        message_type.path = (
            self.path.child_path(message_type.type_name)
            if path is None
            else ProtoMessagePath(path=path.split("."))
        )
        message_type.root = self.root
        self.nested_types[message_type.type_name] = message_type
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
        new_message_t = MessageTypeRules(name=name, fields=fields)

        child = self
        for node in path[:-1]:
            try:
                child = child.nested_types[node]
            except KeyError:
                child = child.add_type(MessageTypeRules(node))

        child.add_type(new_message_t)

        return new_message_t

    def get_type(self, message_path):
        """Get a MessageType by name or path"""
        if isinstance(message_path, ProtoMessagePath):
            message_t = self
            for component in message_path.path:
                try:
                    message_t = message_t.nested_types[component]
                except KeyError:
                    raise KeyError("Type not found: " + str(message_path))
            return message_t
        if isinstance(message_path, str):
            return self.nested_types[message_path]

        sys.stderr.write("Type must be ProtoMessagePath or str" + "\n")

    def __getitem__(self, name):
        return self.nested_types[name]

    def __repr__(self):
        return f"TypeContainer({len(self.nested_types)}):\n" + ",".join(
            map(str, self.nested_types)
        )


class MessageTypeRules(TypeRulesContainer):
    """This class manages the fields of a Message Type"""

    def __init__(self, name, fields=None, root=None):
        super().__init__(root=root)
        self.type_name = name
        self.fields = dict()
        if isinstance(fields, list):
            for field in fields:
                self.fields[field.field_name] = field
        elif isinstance(fields, dict):
            self.fields = fields

    def add_field(self, field):
        """Add a field with or without rules to a Message Type"""
        field.path = self.path.child_path(field.field_name)
        field.root = self.root
        self.fields[field.field_name] = field
        return field

    def get_field(self, field_name):
        return self.fields[field_name]

    def __getitem__(self, field_name):
        return self.get_field(field_name)

    def __repr__(self):
        return (
            f"{self.type_name}:"
            + f"MessageType({len(self.fields)}):{self.fields},"
            + f"Nested types({len(self.nested_types)})"
            + (":" + ",".join(self.nested_types.keys()) if self.nested_types else "")
        )


class FieldRules(OSIRuleNode):
    """This class manages the rules of a Field in a Message Type"""

    def __init__(self, name, rules=None, path=None, root=None):
        super().__init__()
        self.rules = dict()
        self.field_name = name

        if path:
            self.path = path

        if root:
            self.root = root

        if isinstance(rules, list):
            for rule in rules:
                self.add_rule(rule)

    def add_rule(self, rule):
        """Add a new rule to a field with the parameters.
        For example:

        .. code-block:: python

            self.add_rule(Rule(verb="is_less_than_or_equal_to", params=2))

        The rule can also be a dictionary containing one key (the rule verb) with one
        value (the parameter).
        For example:

        .. code-block:: python

            self.add_rule({"is_less_than_or_equal_to": 2})
        """
        rule.path = self.path.child_path(rule.verb)
        rule.root = self.root
        self.rules[rule.verb] = rule

    def has_rule(self, rule):
        """Check if a field has the rule ``rule``"""
        return rule in self.rules

    def list_rules(self):
        """List the rules of a field"""
        return self.rules

    def get_rule(self, verb):
        """Return the rule object for the verb rule_verb in this field."""
        return self.rules[verb]

    def __getitem__(self, verb):
        return self.get_rule(verb)

    def __repr__(self):
        nested_rules = [self.rules[r] for r in self.rules]
        return f"{self.field_name}:Field({len(self.rules)}):{nested_rules}"


class Rule(OSIRuleNode):
    """This class manages one rule"""

    def __init__(self, **kwargs):
        super().__init__()
        self.severity = kwargs.get("severity", Severity.ERROR)
        self.path = kwargs.get("path", ProtoMessagePath())
        self.field_name = kwargs.get("field_name")

        self.params = kwargs.get("params", None)
        self.extra_params = kwargs.get("extra_params", None)
        self.target = kwargs.get("target", None)
        self.verb = kwargs.get("verb", None)

        dictionary = kwargs.get("dictionary", None)
        if dictionary:
            self.from_dict(dictionary)

        if not hasattr(osi_rules_implementations, self.verb):
            sys.stderr.write(self.verb + " rule does not exist\n")

    def from_dict(self, rule_dict: dict):
        """Instantiate Rule object from a dictionary"""
        try:
            (verb, params), *extra_params = rule_dict.items()
            self.verb = verb
            self.params = params
            self.extra_params = dict(extra_params)
            self.target = self.extra_params.pop("target", None)

            return True
        except AttributeError:
            sys.stderr.write("rule must be YAML mapping, got: " + str(rule_dict) + "\n")
        return False

    @property
    def path(self):
        return self._path

    @property
    def targeted_field(self):
        if self.target:
            return self.target.split(".")[-1]
        return self.field_name

    @path.setter
    def path(self, path):
        self._path = path
        if len(self.path.path) >= 2 and isinstance(self.path, ProtoMessagePath):
            self.field_name = self.path.path[-2]
        elif not hasattr(self, "field_name"):
            self.field_name = "UnknownField"

    def __repr__(self):
        return f"{self.verb}({self.params}) target={self.target}"

    def __eq__(self, other):
        return (
            self.verb == other.verb
            and self.params == other.params
            and self.severity == other.severity
        )


class Severity(Enum):
    """Description of the severity of the raised error if a rule does not comply."""

    INFO = 20
    WARN = 30
    ERROR = 40
