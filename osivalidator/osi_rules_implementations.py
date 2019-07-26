"""
This module contains the implementation of each rule to be used in the
requirements or in the Doxygen documentation.

All these rules are bounded into "OSIRulesChecker", so they have access to all
its attributes and methods.
"""
from functools import wraps

from asteval import Interpreter
from iso3166 import countries

from .osi_rules import MessageType, ProtoMessagePath, Field

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


def rule_implementation(func):
    """
    Decorator to label rules method implementations
    """
    func.is_rule = True

    # return func

    # Uncomment for function benchmarking
    # @wraps(func)
    # def wrapper(self, *args, **kwargs):
    #     start = time.time()
    #     with open("benchmark.txt", "a") as benchmark_file:
    #         print(func.__name__, time.time()-start, file=benchmark_file)
    #     return func(self, *args, **kwargs)

    # return wrapper

    @wraps(func)
    def wrapper(self, field, rule_obj, **kwargs):
        result = func(self, field, rule_obj, **kwargs)
        if isinstance(rule_obj, Field):
            rule_obj = rule_obj.rules[func.__name__]
        severity = rule_obj.severity
        params = "" if rule_obj.params is None else f"({rule_obj.params})"
        if not result:
            self.log(
                severity, f'{rule_obj.path}{params} does not comply in '
                + field.path)
        return result

    return wrapper

# RULES


@rule_implementation
def is_valid(self, field, rule):
    """*Rule*

    Check if a field message is valid, that is all the inner rules of the
    message in the field are complying.
    """

    field_type_desc = field.value.DESCRIPTOR
    message_t_inherit = []
    while field_type_desc is not None:
        message_t_inherit.insert(0, field_type_desc.name)
        field_type_desc = field_type_desc.containing_type

    child_rules = self.rules.get_type(ProtoMessagePath(message_t_inherit))
    return self.check_compliance(field, child_rules)


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
def first_element(self, field, rule):
    """*Rule*

    Check rule for first message of a repeated field.

    :param params: dictionary of rules to be checked for the first message
    """
    nested_fields_rules = rule.params

    # Note: Here, the virtual message type get its field name as a name
    virtual_message_rules = MessageType(rule.field_name, nested_fields_rules)
    return self.check_compliance(field[0], virtual_message_rules)


@rule_implementation
def last_element(self, field, rule):
    """*Rule*

    Check rule for last message of a repeated field.

    :param params: dictionary of rules to be checked for the last message
    """
    nested_fields_rules = rule.params
    virtual_message_rules = MessageType(rule.field_name, nested_fields_rules)
    return self.check_compliance(field[-1], virtual_message_rules)


@rule_implementation
@pre_check
def is_set(self, field, rule, **kwargs):
    """*Rule*

    Check if a field is set. The Python function is actually a wrapper of
    ``is_valid``.
    The setting of the field is checked during the exploration of the
    fields.
    """
    if kwargs.get("pre_check", False):
        if not field.has_field(rule.field_name):
            return False
    return True


@rule_implementation
@pre_check
def is_set_if(self, field, rule, **kwargs):
    """*Rule*

    A wrapper to the function ``is_set``. The condition should be contained
    in `params` as a string but is checked during the exploration of the
    message.

    :param params: The assertion in Python-style pseudo-code as a string.
    """
    if kwargs.get("pre_check", False):
        cond = rule['is_set_if'].params
        dict_message = field.dict
        if Interpreter(dict_message)(cond):
            if not field.has_field(rule.name):
                return False

    return True
