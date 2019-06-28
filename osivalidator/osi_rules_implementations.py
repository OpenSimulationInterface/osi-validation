"""
This module contains the implementation of each rule to be used in the
requirements or in the Doxygen documentation.

All these rules are bounded into "OSIRulesChecker", so they have access to all
its attributes and methods.
"""

from asteval import Interpreter
from iso3166 import countries

from google.protobuf.json_format import MessageToDict

from .osi_rules import MessageType, ProtoMessagePath
from .utils import get_message_path, has_attr

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


def rule(func):
    """
    Decorator to label rules method implementations
    """
    func.is_rule = True

    return func

    # Uncomment for function benchmarking
    # @wraps(func)
    # def wrapper(self, *args, **kwargs):
    #     start = time.time()
    #     with open("benchmark.txt", "a") as benchmark_file:
    #         print(func.__name__, time.time()-start, file=benchmark_file)
    #     return func(self, *args, **kwargs)

    # return wrapper

# RULES


@rule
def is_valid(self, inherit, rule_obj):
    """*Rule*

    Check if a field message is valid, that is all the inner rules of the
    message in the field are complying.
    """

    field = inherit[-1][1]

    field_type_desc = field.DESCRIPTOR
    message_t_inherit = []
    while field_type_desc is not None:
        message_t_inherit.insert(0, field_type_desc.name)
        field_type_desc = field_type_desc.containing_type

    self.log("debug", f"Check for compliancy of {rule_obj.path}")

    child_rules = self.rules.get_type(ProtoMessagePath(message_t_inherit))
    return self.check_compliance(inherit, child_rules)


@rule
def is_minimum(self, inherit, rule_obj):
    """*Rule*

    Check if a number is over a minimum.
    """
    severity = rule_obj.severity
    minimum = rule_obj.params

    self.log('debug', f'Minimum: {minimum}')
    value = inherit[-1][1]
    res = value >= minimum
    if not res:
        self.log(severity,
                 f'{get_message_path(inherit)} = {value} is too low ' +
                 f'(minimum: {minimum})')
    return res


@rule
def is_maximum(self, inherit, rule_obj):
    """*Rule*

    Check if a number is under a maximum.

    :param params: the maximum
    """
    severity = rule_obj.severity
    maximum = rule_obj.params

    self.log('debug', f'Maximum: {maximum}')
    value = inherit[-1][1]
    res = value >= maximum
    if not res:
        self.log(severity,
                 f'{get_message_path(inherit)} = {value} is too high ' +
                 f'(maximum: {maximum})')
    return res


@rule
def in_range(self, inherit, rule_obj):
    """*Rule*

    Check if a number is in a range.

    :param params: must be a table. The first element is the minimum, the
                   second element is the maximum. The first element, if
                   present, is a parameter string:

                   - if it contains 'lo', the interval is left-open
                   - if it contains 'ro', the interval is right-open

                   The interval can be 'loro', that is left and right-open.
    """
    severity = rule_obj.severity
    interval = rule_obj.params

    mini = float(interval[0])
    maxi = float(interval[1])
    val = inherit[-1][1]

    is_equal_to_bound = len(interval) >= 3 and (
        str.find(interval[2], 'lo') >= 0 and mini == val or
        str.find(interval[2], 'ro') >= 0 and maxi == val
    )

    result = mini <= val <= maxi and not is_equal_to_bound

    n_in = "not " if not result else ""

    message_model = \
        f'{get_message_path(inherit)}= {val} {n_in}in range: {mini, maxi}'

    log_severity = "debug" if result else severity
    self.log(log_severity, message_model)
    return result


@rule
def is_global_unique(self, inherit, rule_obj):
    """*Rule*

    Register an ID in the OSI ID manager to later perform a ID
    consistency validation.

    Must be set to an Identifier.
    """

    object_of_id = inherit[-2][1]
    identifier = inherit[-1][1].value

    self.log("debug", f"Check for uniqueness of {rule_obj.path}")

    return self.id_manager.register_message(identifier, object_of_id)


@rule
def refers(self, inherit, rule_obj):
    """*Rule*

    Add a reference to another message by ID.

    **TODO**: the conditional reference. Still no case of use in OSI let
    this pending.

    :param params: id of the refered object
    """
    expected_type = rule_obj.params

    referer = inherit[-2][1]
    identifier = inherit[-1][1].value
    condition = None
    self.id_manager.refer(referer, identifier, expected_type, condition)
    return True


@rule
def is_iso_country_code(self, inherit, rule_obj):
    """*Rule*

    Check if a string is a ISO country code.
    """
    severity = rule_obj.severity

    self.log('debug', f'Checking ISO code for {inherit[-1][1]}')
    iso_code = inherit[-1][1]
    try:
        countries.get(iso_code)
        self.log("debug", f'ISO code {iso_code} is valid')
        return True
    except KeyError:
        self.log(severity, f'ISO code {iso_code} is not valid')
        return False


@rule
def first_element(self, inherit, rule_obj):
    """*Rule*

    Check rule for first message of a repeated field.

    :param params: dictionary of rules to be checked for the first message
    """
    nested_fields_rules = rule_obj.params
    virtual_message = MessageType('', nested_fields_rules)
    return self.check_compliance(
        inherit + [(None, inherit[-1][1][0])], virtual_message)


@rule
def last_element(self, inherit, rule_obj):
    """*Rule*

    Check rule for last message of a repeated field.

    :param params: dictionary of rules to be checked for the last message
    """
    nested_fields_rules = rule_obj.params

    virtual_message = MessageType('', nested_fields_rules)
    return self.check_compliance(
        inherit + [(None, inherit[-1][1][-1])], virtual_message)


@rule
@pre_check
def is_set(self, inherit, rule_obj, **kwargs):
    """*Rule*

    Check if a field is set. The Python function is actually a wrapper of
    ``is_valid``.
    The setting of the field is checked during the exploration of the
    fields.
    """
    if kwargs.get("pre_check", False):
        if not has_attr(inherit[-1][1], rule_obj.name):
            self.log(rule_obj.rules['is_set'].severity,
                     f"{rule_obj.path} is not set!")
            return False
        return True
    if hasattr(inherit[-1][1], "DESCRIPTOR"):
        return self.is_valid(inherit, rule_obj)
    return True


@rule
@pre_check
def is_set_if(self, inherit, rule_obj, **kwargs):
    """*Rule*

    A wrapper to the function ``is_set``. The condition should be contained
    in `params` as a string but is checked during the exploration of the
    message.

    :param params: The assertion in Python-style pseudo-code as a string.
    """
    if kwargs.get("pre_check", False):
        dict_message_cont = kwargs.get("dict_message_cont", None)
        message = inherit[-1][1]
        cond = rule_obj['is_set_if'].params
        dict_message_cont[0] = dict_message_cont[0] or MessageToDict(
            message, preserving_proto_field_name=True,
            use_integers_for_enums=True)
        if (Interpreter(dict_message_cont[0])(cond) and
                not has_attr(message, rule_obj.name)):
            self.log(rule_obj.rules['is_set_if'].severity,
                     f"{rule_obj.path} not set as expected: " +
                     f"{cond}")
            return False
        return True

    return self.is_set(inherit, rule_obj)
