"""
This module contains the implementation of each rule to be used in the
requirements or in the Doxygen documentation.

All these rules are bounded into "OSIRulesChecker", so they have access to all
its attributes and methods.
"""

from functools import wraps
from iso3166 import countries
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import osi_rules


def add_default_rules_to_subfields(message, type_rules):
    """Add default rules to fields of message fields (subfields)"""
    for descriptor in message.all_field_descriptors:
        field_rules = (
            type_rules.get_field(descriptor.name)
            if descriptor.name in type_rules.fields
            else type_rules.add_field(osi_rules.FieldRules(descriptor.name))
        )

        if descriptor.message_type:
            field_rules.add_rule(osi_rules.Rule(verb="is_valid"))

        is_set_severity = (
            osi_rules.Severity.WARN
            if field_rules.has_rule("is_optional")
            else osi_rules.Severity.ERROR
        )

        field_rules.add_rule(osi_rules.Rule(verb="is_set", severity=is_set_severity))


# DECORATORS
# These functions are no rule implementation, but decorators to characterize
# rules. These decorators can also be used to make grouped checks like
# benchmarks.


def pre_check(func):
    """Decorator for rules that need to be checked before knowing that the field
    exists or not
    """
    func.pre_check = True
    return func


def repeated_selector(func):
    """Decorator for selector-rules that take"""
    func.repeated_selector = True
    return func


def rule_implementation(func):
    """Decorator to label rules method implementations"""
    func.is_rule = True

    @wraps(func)
    def wrapper(self, field, rule, **kwargs):
        if isinstance(rule, osi_rules.FieldRules):
            rule = rule.rules[func.__name__]

        if isinstance(field, list) and not getattr(func, "repeated_selector", False):
            result = all([func(self, unique_field, rule) for unique_field in field])
        else:
            result = func(self, field, rule, **kwargs)

        if not result and isinstance(rule, osi_rules.Rule):
            if isinstance(field, list):
                path = field[0].path
            else:
                path = field.path
            self.log(
                rule.severity,
                str(rule.path)
                + "("
                + str(rule.params)
                + ")"
                + " does not comply in "
                + str(path),
            )

        return result

    return wrapper


# RULES
# TODO Refactor this code into a seperate class so it can be easy parsed by sphinx

# Special type matching for paths
type_match = {
    "moving_object.base": "BaseMoving",
    "stationary_object.base": "BaseStationary",
}


@rule_implementation
def is_valid(self, field, rule):
    """Check if a field message is valid, that is all the inner rules of the
    message in the field are complying.

    :param params: none
    """
    path_list = field.path.split(".")
    type_structure = None
    if len(path_list) > 2:
        grandparent = path_list[-3]
        parent = path_list[-2]
        child = path_list[-1]
        type_structure = type_match.get(grandparent + "." + parent)

    if type_structure and child in rule.root.get_type(type_structure).nested_types:
        subfield_rules = rule.root.get_type(type_structure).nested_types[child]
    # subfield_rules = rule.root.get_type(field.message_type)
    elif isinstance(rule, osi_rules.MessageTypeRules):
        subfield_rules = rule
    else:
        subfield_rules = rule.root.get_type(field.message_type)

    result = True
    # Add default rules for each subfield that can be validated (default)
    add_default_rules_to_subfields(field, subfield_rules)

    # loop over the fields in the rules
    for subfield_rules in subfield_rules.fields.values():
        for subfield_rule in subfield_rules.rules.values():
            result = self.check_rule(field, subfield_rule) and result

        # Resolve ID and references
    if not field.parent:
        self.id_manager.resolve_unicity(self.timestamp)
        self.id_manager.resolve_references(self.timestamp)
    return result


@rule_implementation
def is_less_than_or_equal_to(self, field, rule):
    """Check if a number is under or equal a maximum.

    :param params: the maximum (float)
    """
    return field.value <= rule.params


@rule_implementation
def is_less_than(self, field, rule):
    """Check if a number is under a maximum.

    :param params: the maximum (float)
    """
    return field.value < rule.params


@rule_implementation
def is_greater_than_or_equal_to(self, field, rule):
    """Check if a number is over or equal a minimum.

    :param params: the minimum (float)
    """
    return field.value >= rule.params


@rule_implementation
def is_greater_than(self, field, rule):
    """Check if a number is over a minimum.

    :param params: the minimum (float)
    """
    return field.value > rule.params


@rule_implementation
def is_equal_to(self, field, rule):
    """Check if a number equals the parameter.

    :param params: the equality to check (float or bool)

    Example:
    ```
    - is_equal_to: 1
    ```
    """
    return field.value == rule.params


@rule_implementation
def is_different_to(self, field, rule):
    """Check if a number is different from the parameter.

    :param params: the inequality to check (float or bool)

    Example:
    ```
    - is_different_to: 1
    ```
    """
    return field.value != rule.params


@rule_implementation
def is_globally_unique(self, field, rule):
    """Register an ID in the OSI ID manager to later perform a ID
    consistency validation.

    Must be set to an Identifier.

    :param params: none
    """

    object_of_id = field.parent.value
    identifier = field.value.value

    return self.id_manager.register_message(identifier, object_of_id)


@rule_implementation
def refers_to(self, field, rule):
    """Add a reference to another message by ID.

    :param params: Type name of the referred object (string)
    """
    expected_type = rule.params

    referer = field.parent.value
    identifier = field.value.value
    condition = None
    self.id_manager.refer(referer, identifier, expected_type, condition)
    return True


@rule_implementation
def is_iso_country_code(self, field, rule):
    """Check if a string is a ISO country code.

    :param params: none
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
    """Check rule for first message of a repeated field.

    :param params: dictionary of rules to be checked for the first message
                   (mapping)
    """
    statement_true = True
    nested_fields_rules = rule.params

    # Convert parsed yaml file to dictonary rules
    nested_fields_rules_list = []
    for key_field, nested_rule in nested_fields_rules.items():
        nested_rule[0].update({"target": "this." + key_field})
        nested_fields_rules_list.append(nested_rule[0])

    rules_checker_list = []
    for nested_fields_rule in nested_fields_rules_list:
        statement_rule = osi_rules.Rule(
            dictionary=nested_fields_rule,
            field_name=rule.field_name,
            severity=osi_rules.Severity.ERROR,
        )
        statement_rule.path = rule.path.child_path(statement_rule.verb)
        statement_true = self.check_rule(field[0], statement_rule) and statement_true
        rules_checker_list.append(statement_true)

    return all(rules_checker_list)


@rule_implementation
@repeated_selector
def last_element(self, field, rule):
    """Check rule for last message of a repeated field.

    :param field: Field to which the rule needs to comply
    :param rule: dictionary of rules to be checked for the last message
                   (mapping)
    """
    statement_true = True
    nested_fields_rules = rule.params

    # Convert parsed yaml file to dictonary rules
    nested_fields_rules_list = []
    for key_field, nested_rule in nested_fields_rules.items():
        nested_rule[0].update({"target": "this." + key_field})
        nested_fields_rules_list.append(nested_rule[0])

    rules_checker_list = []
    for nested_fields_rule in nested_fields_rules_list:
        statement_rule = osi_rules.Rule(
            dictionary=nested_fields_rule,
            field_name=rule.field_name,
            severity=osi_rules.Severity.ERROR,
        )
        statement_rule.path = rule.path.child_path(statement_rule.verb)
        statement_true = self.check_rule(field[-1], statement_rule) and statement_true
        rules_checker_list.append(statement_true)

    return all(rules_checker_list)


@rule_implementation
def is_optional(self, field, rule):
    """This rule set the is_set one on a "Warning" severity.

    :param params: none
    """
    return True


@rule_implementation
@pre_check
def is_set(self, field, rule):
    """Check if a field is set or if a repeated field has at least one element.

    :param params: none
    """
    return field.has_field(rule.field_name)


@rule_implementation
@pre_check
def check_if(self, field, rule):
    """
    Evaluate rules if some statements are verified:

    :param params: statements
    :param extra_params: `do_check`: rules to validate if statements are true

    Structure:

    a_field:
    - check_if:
    {params: statements}
    do_check:
    {extra_params: rules to validate if statements are true}


    Example:

    a_field:
    - check_if:
    - is_set: # Statements
    target: parent.environment.temperature
    - another_statement: statement parameter
    do_check: # Check that will be performed only if the statements are True
    - is_less_than_or_equal_to: 0.5
    - is_greater_than_or_equal_to: 0

    """
    statements = rule.params
    do_checks = rule.extra_params["do_check"]
    statement_true = True

    # Check if all the statements are true
    for statement in statements:
        statement_rule = osi_rules.Rule(
            dictionary=statement,
            field_name=rule.field_name,
            severity=osi_rules.Severity.INFO,
        )
        statement_rule.path = rule.path.child_path(statement_rule.verb)
        statement_true = self.check_rule(field, statement_rule) and statement_true

    # If the statements are true, check the do_check rules
    if not statement_true:
        return True

    return all(
        (
            self.check_rule(
                field,
                osi_rules.Rule(
                    path=rule.path.child_path(next(iter(check.keys()))),
                    dictionary=check,
                    field_name=rule.field_name,
                ),
            )
            for check in do_checks
        )
    )
