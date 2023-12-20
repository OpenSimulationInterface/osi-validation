"""
This module contains all the rules which a message or an attribute of a message
from an OSI trace can comply.
"""

from types import MethodType
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

import osi_rules
import osi_validator_logger
import osi_id_manager
import osi_rules_implementations


class OSIRulesChecker:
    """This class contains all the available rules to write OSI requirements and
    the necessary methods to check their compliance.

    The rule methods are marked with \*Rule\*.
    """

    def __init__(self, logger=None):
        self.logger = logger or osi_validator_logger.OSIValidatorLogger()
        self.id_manager = osi_id_manager.OSIIDManager(logger)
        self.timestamp = self.timestamp_ns = -1

        for module_name in dir(osi_rules_implementations):
            method = getattr(osi_rules_implementations, module_name)
            if getattr(method, "is_rule", False):
                setattr(self, module_name, MethodType(method, self))

    # Rules implementation
    def log(self, severity, message):
        """
        Wrapper for the logger of the Validation Software
        """
        if isinstance(severity, osi_rules.Severity):
            severity_method = osi_validator_logger.SEVERITY[severity]
        elif isinstance(severity, str):
            severity_method = severity
        else:
            raise TypeError("type not accepted: must be Severity enum or str")

        return getattr(self.logger, severity_method)(self.timestamp, message)

    def set_timestamp(self, timestamp, ts_id):
        """Set the timestamp for the analysis"""
        self.timestamp_ns = int(timestamp.nanos + timestamp.seconds * 10e9)
        self.timestamp = ts_id
        return self.timestamp, ts_id

    def check_rule(self, parent_field, rule):
        """Check if a field comply with a rule given the \*parent\* field"""
        try:
            rule_method = getattr(self, rule.verb)
        except AttributeError:
            raise AttributeError("Rule " + rule.verb + " not implemented yet\n")

        if rule.target is not None:
            parent_field = parent_field.query(rule.target, parent=True)

        if getattr(rule_method, "pre_check", False):
            # We do NOT know if the child exists
            checked_field = parent_field
        elif parent_field.has_field(rule.targeted_field):
            # We DO know that the child exists
            checked_field = parent_field.get_field(rule.targeted_field)
        else:
            checked_field = None

        if checked_field is not None:
            return rule_method(checked_field, rule)

        return False
