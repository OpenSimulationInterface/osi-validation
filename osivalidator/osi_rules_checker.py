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
            method
            for method in dir(osi_rules_implementations)
            if getattr(
                getattr(osi_rules_implementations, method),
                'is_rule',
                False
            )
        ]

        for verb in verb_list:
            setattr(self, verb, MethodType(
                getattr(osi_rules_implementations, verb), self))

        self.pre_check_rules = [method for method in dir(
            self) if getattr(getattr(self, method), "pre_check", False)]

    # Rules implementation

    def _check_repeated(self, message_list, rule):
        rule_method = getattr(self, rule.verb)
        verb = rule_method.__name__

        self.log('debug',
                 f'Check the rule {verb} for a repeated field')

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

    def check_compliance(self, linked_message, rules):
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
        message = linked_message
        dict_message_cont = [None]

        add_default_rules(message, rules)

        # loop over the fields in the rules
        for field_name, rules_field_node in rules.fields.items():
            field_path = rules_field_node.path

            for verb in self.pre_check_rules:
                if rules_field_node.has_rule(verb):
                    getattr(self, verb)(linked_message, rules_field_node,
                                        pre_check=True,
                                        dict_message_cont=dict_message_cont)

            if not has_attr(message, field_name):
                self.log('debug', f'Field {field_path} does not exist')
                continue

            res = self._loop_over_rules(
                rules_field_node, linked_message[field_name])

            final_res = False if not res else final_res

        # Resolve ID and references
        if not linked_message.GetParent:
            self.id_manager.resolve_unicity(self.timestamp)
            self.id_manager.resolve_references(self.timestamp)
        return final_res

    def _loop_over_rules(self, field_rules, linked_message):
        final_res = True
        for _, rule_obj in field_rules.rules.items():
            verb = rule_obj.verb

            try:
                rule_method = getattr(self, verb)
            except AttributeError:
                self.log('error', f'Rule "{verb}" not implemented yet!')
            else:
                # If the field is "REPEATED"
                if isinstance(linked_message, list):
                    first_elt = linked_message[0]
                    if(self.ignore_lanes
                       and first_elt.GetFieldName() == 'lane_boundary'
                       and isinstance(
                           first_elt.GetParent().GetProtoNode(),
                           GroundTruth
                       )):
                        continue
                    res = self._check_repeated(linked_message, rule_obj)
                else:
                    res = rule_method(linked_message, rule_obj)

                final_res = final_res if res else False
        return final_res


def add_default_rules(message, rules):
    """Add "is_valid" rule to all the field of message without is_set or
    is_valid
    """
    def is_validable(message):
        return message.IsMessage()
    for linked_message in filter(is_validable, message.ListFields()):
        if linked_message.GetFieldName() not in rules.fields:
            rules.add_field(Field(linked_message.GetFieldName())
                            ).add_rule(Rule('is_valid'))
        else:
            rules.get_field(linked_message.GetFieldName()
                            ).add_rule(Rule('is_valid'))
