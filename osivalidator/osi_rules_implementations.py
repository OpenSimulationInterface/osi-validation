"""
This module contains the implementation of each rule to be used in the
requirements or in the Doxygen documentation.

All these rules are bounded into "OSIRulesChecker", so they have access to all
its attributes and methods.
"""
from functools import wraps

from asteval import Interpreter
from iso3166 import countries

from .osi_rules import MessageTypeRules, FieldRules, Severity, Rule


def add_default_rules_to_subfields(message, type_rules):
    """Add default rules to fields of message fields (subfields)
    """
    for field in message.fields:
        field_rules = (type_rules.get_field(field.name)
                       if field.name in type_rules.fields
                       else type_rules.add_field(FieldRules(field.name)))

        if field.is_message:
            field_rules.add_rule(Rule('is_valid'))

        is_set_severity = (Severity.WARN
                           if field_rules.has_rule('is_optional')
                           else Severity.ERROR)

        field_rules.add_rule(Rule('is_set', severity=is_set_severity))


# DECORATORS
# These functions are no rule implementation, but decorators to characterize
# rules. These decorators can also be used to make grouped checks like
# benchmarks.


def pre_check(func):
    """
    Decorator for rules that need to be checked before knowing that the field
    exists or not
    """
    func.pre_check = True
    return func


def repeated_selector(func):
    """
    Decorator for selector-rules that take
    """
    func.repeated_selector = True
    return func


def rule_implementation(func):
    """
    Decorator to label rules method implementations
    """
    func.is_rule = True
    @wraps(func)
    def wrapper(self, field, rule, **kwargs):
        if isinstance(field, list) and not func.repeated_selector:
            result = all([func(unique_field, rule) for unique_field in field])
        else:
            result = func(self, field, rule, **kwargs)

        if isinstance(rule, FieldRules):
            rule = rule.rules[func.__name__]
        if not result and isinstance(rule, Rule):
            self.log(rule.severity, str(rule.path) + '(' + str(rule.params) + ')'
                     + ' does not comply in ' + str(field.path))
        return result

    return wrapper


# RULES


@rule_implementation
def is_valid(self, field, rule):
    """*Rule*

    Check if a field message is valid, that is all the inner rules of the
    message in the field are complying.
    """
    subfield_rules = rule.root.get_type(field.message_type)

    result = True
    # Add default rules for each subfield that can be validated (default)
    add_default_rules_to_subfields(field, subfield_rules)

    # loop over the fields in the rules
    for subfield_name, subfield_rules in subfield_rules.fields.items():
        for verb in self.pre_check_rules:
            if subfield_rules.has_rule(verb):
                getattr(self, verb)(field, subfield_rules.get_rule(verb),
                                    pre_check=True)

        if not field.has_field(subfield_name):
            continue

        for subfield_rule in subfield_rules.rules.values():
            try:
                result = (getattr(self, subfield_rule.verb)(
                    field.get_field(subfield_name), subfield_rule) and result)
            except AttributeError:
                self.log('error',
                         f'Rule "{subfield_rule.verb}" not implemented yet')

    # Resolve ID and references
    if not field.parent:
        self.id_manager.resolve_unicity(self.timestamp)
        self.id_manager.resolve_references(self.timestamp)
    return result


@rule_implementation
def is_less_than_or_equal_to(self, field, rule):
    """*Rule*

    Check if a number is under or equal a maximum.

    :param params: the maximum
    """
    return field.value <= rule.params


@rule_implementation
def is_less_than(self, field, rule):
    """*Rule*

    Check if a number is under a maximum.

    :param params: the maximum
    """
    return field.value < rule.params


@rule_implementation
def is_greater_than_or_equal_to(self, field, rule):
    """*Rule*

    Check if a number is over or equal a minimum.

    :param params: the maximum
    """
    return field.value >= rule.params


@rule_implementation
def is_greater_than(self, field, rule):
    """*Rule*

    Check if a number is over a minimum.

    :param params: the maximum
    """
    return field.value > rule.params


@rule_implementation
def is_global_unique(self, field, rule):
    """*Rule*

    Register an ID in the OSI ID manager to later perform a ID
    consistency validation.

    Must be set to an Identifier.
    """

    object_of_id = field.parent.value
    identifier = field.value.value

    return self.id_manager.register_message(identifier, object_of_id)


@rule_implementation
def refers(self, field, rule):
    """*Rule*

    Add a reference to another message by ID.

    **TODO**: the conditional reference. Still no case of use in OSI let
    this pending.

    :param params: id of the refered object
    """
    expected_type = rule.params

    referer = field.parent.value
    identifier = field.value.value
    condition = None
    self.id_manager.refer(referer, identifier, expected_type, condition)
    return True


@rule_implementation
def is_iso_country_code(self, field, rule):
    """*Rule*

    Check if a string is a ISO country code.
    """
    iso_code = field
    try:
        countries.get(iso_code)
        return True
    except KeyError:
        return False


@rule_implementation
@repeated_selector
def first_element(self, field, rule):
    """*Rule*

    Check rule for first message of a repeated field.

    :param params: dictionary of rules to be checked for the first message
    """
    nested_fields_rules = rule.params

    # Note: Here, the virtual message type get its field name as a name
    virtual_message_rules = MessageTypeRules(
        rule.field_name, nested_fields_rules)
    return self.is_valid(field[0], virtual_message_rules)


@rule_implementation
@repeated_selector
def last_element(self, field, rule):
    """*Rule*

    Check rule for last message of a repeated field.

    :param params: dictionary of rules to be checked for the last message
    """
    nested_fields_rules = rule.params
    virtual_message_rules = MessageTypeRules(
        rule.field_name, nested_fields_rules)
    return self.is_valid(field[-1], virtual_message_rules)


@rule_implementation
def is_optional(self, field, rule):
    """*Rule*

    This rule set the is_set one on a "Warning" severity.
    """
    return True


@rule_implementation
@pre_check
def is_set(self, field, rule, **kwargs):
    """*Rule*

    Check if a field is set. The Python function is actually a wrapper of
    ``is_valid``.
    The setting of the field is checked during the exploration of the
    fields.
    """
    return (not kwargs.get("pre_check", False)
            or field.has_field(rule.field_name))


@rule_implementation
@pre_check
def is_set_if(self, field, rule, **kwargs):
    """*Rule*

    Conditional version of is_set The condition should be contained
    in `params` as a string but is checked during the exploration of the
    message.

    :param params: The assertion in Python-style pseudo-code as a string.
    """
    if kwargs.get("pre_check", False):
        condition = rule['is_set_if'].params
        return (not Interpreter(field.to_dict())(condition)
                or field.has_field(rule.name))  # Logical implication

    return True
