"""
This module contains all the rules which a message or an attribute of a message
from an OSI scenario can comply.
"""

from types import MethodType

from osi3.osi_groundtruth_pb2 import GroundTruth

from .osi_rules import Severity, Rule, Field
from .osi_validator_logger import SEVERITY
from .osi_id_manager import OSIIDManager
from . import osi_rules_implementations
from .utils import has_attr


class OSIRulesChecker:
    """This class contains all the available rules to write OSI requirements and
    the necessary methods to check their compliance.

    The rule methods are marked with *Rule*.
    """

    def __init__(self, ovr, logger, ignore_lanes):
        self.rules = ovr.t_rules
        self.logger = logger
        self.id_manager = OSIIDManager(logger)
        self.timestamp = self.timestamp_ns = -1
        self.ignore_lanes = ignore_lanes

        verb_list = [
            m
            for m in dir(osi_rules_implementations)
            if getattr(getattr(osi_rules_implementations, m), 'is_rule', False)
        ]

        for verb in verb_list:
            setattr(self, verb, MethodType(
                getattr(osi_rules_implementations, verb), self))

        self.pre_check_rules = [method for method in dir(
            self) if getattr(getattr(self, method), "pre_check", False)]

    # Rules implementation

    def _check_repeated(self, inherit, rule):
        rule_method = getattr(self, rule.verb)
        verb = rule_method.__name__

        self.log('debug',
                 f'Check the rule {verb} for a repeated field')

        if verb in ['first_element', 'last_element']:
            return rule_method(inherit, rule)

        return all([
            rule_method(inherit + [(None, m)], rule) for m in inherit[-1][1]])

    def log(self, severity, message):
        """
        Wrapper for the logger of the Validation Software
        """
        if isinstance(severity, Severity):
            severity_method = SEVERITY[severity]
        elif isinstance(severity, str):
            severity_method = severity
        else:
            raise TypeError('type not accepted: must be Severity enum or str')

        return getattr(self.logger, severity_method)(self.timestamp, message)

    def set_timestamp(self, timestamp, ts_id):
        """Set the timestamp for the analysis"""
        self.timestamp_ns = int(timestamp.nanos + timestamp.seconds * 10e9)
        self.timestamp = ts_id
        return self.timestamp, ts_id

    def check_compliance(self, inherit, rules):
        """Method to check the rules for a complex message
        It is also the input method

        :param inherit: a list representing the inheritance of the processed
                        message in tuples
        :param rules: the dictionary for the rules rooted at the type of the
                      processed message

        .. note:: inherit parameter must have this structure:
                  ``[(None, Root message), (Field descriptor, Child message),
                  ...]``

                  The last tuple represents the processed message.
        """
        final_res = True
        # Add "is_valid" rule for each field that can be validated (default)
        message = inherit[-1][1]
        dict_message_cont = [None]

        add_default_valid_rules(message, rules)

        # loop over the fields in the rules
        # if the name starts with an upper char, it is a submessage type
        for field_name, rules_field_node in rules.fields.items():
            field_path = rules_field_node.path

            for verb in self.pre_check_rules:
                if rules_field_node.has_rule(verb):
                    getattr(self, verb)(inherit, rules_field_node,
                                        pre_check=True,
                                        dict_message_cont=dict_message_cont)

            if not has_attr(message, field_name):
                self.log('debug', f'Field {field_path} does not exist')
                continue

            proto_field_tuple = next(
                filter(lambda t, fn=field_name: t[0].name == fn,
                       message.ListFields()))
            child_inherit = inherit + [proto_field_tuple]

            res = self._loop_over_rules(rules_field_node, child_inherit)

            final_res = False if not res else final_res

        # Resolve ID and references
        if len(inherit) == 1:
            self.id_manager.resolve_unicity(self.timestamp)
            self.id_manager.resolve_references(self.timestamp)
        return final_res

    def _loop_over_rules(self, field_rules, child_inherit):
        final_res = True
        for _, rule_obj in field_rules.rules.items():
            verb = rule_obj.verb

            try:
                rule_method = getattr(self, verb)
            except AttributeError:
                self.log('error', f'Rule "{verb}" not implemented yet!')
            else:
                # If the field is "REPEATED"
                if child_inherit[-1][0].label == 3:
                    if (self.ignore_lanes and
                            child_inherit[-1][0].name == 'lane_boundary' and
                            isinstance(child_inherit[-2][1], GroundTruth)):
                        continue
                    res = self._check_repeated(child_inherit, rule_obj)
                else:
                    res = rule_method(child_inherit, rule_obj)

                final_res = final_res if res else False
        return final_res


def add_default_valid_rules(message, rules):
    """Add "is_valid" rule to all the field of message without is_set or
    is_valid
    """
    def is_validable(message):
        return message[0].message_type is not None
    for desc, _ in filter(is_validable, message.ListFields()):
        if desc.name not in rules.fields:
            rules.add_field(Field(desc.name))
            rules.get_field(desc.name).add_rule(Rule('is_valid'))
        elif not rules.fields[desc.name].has_rule('is_set'):
            rules.get_field(desc.name).add_rule(Rule('is_valid'))
