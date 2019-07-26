"""
This module contains all the rules which a message or an attribute of a message
from an OSI scenario can comply.
"""

from types import MethodType

from osi3.osi_groundtruth_pb2 import GroundTruth

from .osi_rules import Severity, Rule, Field
from .osi_validator_logger import SEVERITY
from .osi_id_manager import OSIIDManager
from . import osi_rules_implementations as rule_implementations


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
            method for method in dir(rule_implementations)
            if getattr(getattr(rule_implementations, method), 'is_rule', False)
        ]

        for verb in verb_list:
            setattr(self, verb, MethodType(
                getattr(rule_implementations, verb), self))

        self.pre_check_rules = [method for method in dir(
            self) if getattr(getattr(self, method), "pre_check", False)]

    # Rules implementation

    def _check_repeated(self, message_list, rule):
        rule_method = getattr(self, rule.verb)
        verb = rule_method.__name__

        self.log('debug', f'Check the rule {verb} for a repeated field')

        if verb in ['first_element', 'last_element']:
            return rule_method(message_list, rule)

        return all([rule_method(message, rule) for message in message_list])

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

    def check_compliance(self, field, rules):
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
        final_result = True
        # Add "is_valid" rule for each field that can be validated (default)
        add_default_rules(field, rules)

        # loop over the fields in the rules
        for field_name, field_rules in rules.fields.items():
            field_path = field_rules.path

            for verb in self.pre_check_rules:
                if field_rules.has_rule(verb):
                    getattr(self, verb)(field, field_rules, pre_check=True)

            if not field.has_field(field_name):
                self.log('debug', f'Field {field_path} does not exist')
                continue

            result = self._loop_over_rules(field_rules, field[field_name])
            final_result = False if not result else final_result

        # Resolve ID and references
        if not field.parent:
            self.id_manager.resolve_unicity(self.timestamp)
            self.id_manager.resolve_references(self.timestamp)
        return final_result

    def _loop_over_rules(self, field_rules, field):
        final_result = True
        for _, rule in field_rules.rules.items():
            try:
                rule_method = getattr(self, rule.verb)
            except AttributeError:
                self.log('error', f'Rule "{rule.verb}" not implemented yet')
            else:
                # If the field is "REPEATED"
                if isinstance(field, list):
                    if(self.ignore_lanes and field[0].name == 'lane_boundary'
                       and isinstance(field[0].parent.value, GroundTruth)):
                        continue
                    result = self._check_repeated(field, rule)
                else:
                    result = rule_method(field, rule)

                final_result = final_result if result else False
        return final_result


def add_default_rules(field, rules):
    """Add "is_valid" rule to all the field of message without is_set or
    is_valid
    """
    for field in filter(lambda f: f.is_message, field.fields.values()):
        if field.name not in rules.fields:
            rules.add_field(Field(field.name)).add_rule(Rule('is_valid'))
        else:
            rules.get_field(field.name).add_rule(Rule('is_valid'))
