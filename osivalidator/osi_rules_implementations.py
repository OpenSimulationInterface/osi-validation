"""
This module contains the implementation of each rule to be used in the
requirements or in the Doxygen documentation.

All these rules are bounded into "OSIRulesChecker", so they have access to all
its attributes and methods.
"""
from functools import wraps

from asteval import Interpreter
from iso3166 import countries

from google.protobuf.json_format import MessageToDict

from .osi_rules import MessageType, ProtoMessagePath, Rule
from .utils import has_attr

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
    def wrapper(self, linked_message, rule_obj, **kwargs):
        result = func(self, linked_message, rule_obj, **kwargs)
        if isinstance(rule_obj, Rule):
            severity = rule_obj.severity
            params = "" if rule_obj.params is None else f"({rule_obj.params})"
            verb = rule_obj.verb
            if not result:
                self.log(
                    severity,
                    f'{linked_message.GetPath()}: {verb}{params} does not comply')
        return result

    return wrapper
# RULES


@rule
def is_valid(self, linked_message, rule_obj):
    """*Rule*

    Check if a field message is valid, that is all the inner rules of the
    message in the field are complying.
    """

    field = linked_message

    field_type_desc = field.DESCRIPTOR
    message_t_inherit = []
    while field_type_desc is not None:
        message_t_inherit.insert(0, field_type_desc.name)
        field_type_desc = field_type_desc.containing_type

    child_rules = self.rules.get_type(ProtoMessagePath(message_t_inherit))
    return self.check_compliance(linked_message, child_rules)


@rule
def is_minimum(self, linked_message, rule_obj):
    """*Rule*

    Check if a number is over a minimum.
    """
    severity = rule_obj.severity
    minimum = rule_obj.params

    value = linked_message
    res = float(value) >= minimum
    return res


@rule
def is_maximum(self, linked_message, rule_obj):
    """*Rule*

    Check if a number is under a maximum.

    :param params: the maximum
    """
    severity = rule_obj.severity
    maximum = rule_obj.params

    value = linked_message
    res = float(value) <= maximum
    return res


@rule
def in_range(self, linked_message, rule_obj):
    """*Rule*

    Check if a number is in a range.

    :param params: must be a table. The first element is the minimum, the
                   second element is the maximum. The first element, if
                   present, is a parameter string:

                   - if it contains 'lo', the interval is left-open
                   - if it contains 'ro', the interval is right-open

                   The interval can be 'loro', that is left and right-open.
    """
    interval = rule_obj.params

    mini = float(interval[0])
    maxi = float(interval[1])
    val = float(linked_message)

    is_equal_to_bound = len(interval) >= 3 and (
        str.find(interval[2], 'lo') >= 0 and mini == val or
        str.find(interval[2], 'ro') >= 0 and maxi == val
    )

    result = mini <= val <= maxi and not is_equal_to_bound

    return result


@rule
def is_global_unique(self, linked_message, rule_obj):
    """*Rule*

    Register an ID in the OSI ID manager to later perform a ID
    consistency validation.

    Must be set to an Identifier.
    """

    object_of_id = linked_message.GetParent().GetProtoNode()
    identifier = linked_message.GetProtoNode().value

    return self.id_manager.register_message(identifier, object_of_id)


@rule
def refers(self, linked_message, rule_obj):
    """*Rule*

    Add a reference to another message by ID.

    **TODO**: the conditional reference. Still no case of use in OSI let
    this pending.

    :param params: id of the refered object
    """
    expected_type = rule_obj.params

    referer = linked_message.GetParent().GetProtoNode()
    identifier = linked_message.GetProtoNode().value
    condition = None
    self.id_manager.refer(referer, identifier, expected_type, condition)
    return True


@rule
def is_iso_country_code(self, linked_message, rule_obj):
    """*Rule*

    Check if a string is a ISO country code.
    """
    severity = rule_obj.severity
    iso_code = linked_message
    try:
        countries.get(iso_code)
        return True
    except KeyError:
        return False


@rule
def first_element(self, linked_message, rule_obj):
    """*Rule*

    Check rule for first message of a repeated field.

    :param params: dictionary of rules to be checked for the first message
    """
    nested_fields_rules = rule_obj.params
    virtual_message_rules = MessageType('', nested_fields_rules)
    return self.check_compliance(linked_message[0], virtual_message_rules)


@rule
def last_element(self, linked_message, rule_obj):
    """*Rule*

    Check rule for last message of a repeated field.

    :param params: dictionary of rules to be checked for the last message
    """
    nested_fields_rules = rule_obj.params

    virtual_message_rules = MessageType('', nested_fields_rules)
    return self.check_compliance(linked_message[-1], virtual_message_rules)


@rule
@pre_check
def is_set(self, linked_message, rule_obj, **kwargs):
    """*Rule*

    Check if a field is set. The Python function is actually a wrapper of
    ``is_valid``.
    The setting of the field is checked during the exploration of the
    fields.
    """
    if kwargs.get("pre_check", False):
        if not has_attr(linked_message.GetProtoNode(), rule_obj.name):
            self.log(rule_obj.rules['is_set'].severity,
                     f"{rule_obj.path} is not set!")
            return False
    return True


@rule
@pre_check
def is_set_if(self, linked_message, rule_obj, **kwargs):
    """*Rule*

    A wrapper to the function ``is_set``. The condition should be contained
    in `params` as a string but is checked during the exploration of the
    message.

    :param params: The assertion in Python-style pseudo-code as a string.
    """
    if kwargs.get("pre_check", False):
        dict_message_cont = kwargs.get("dict_message_cont", None)
        message = linked_message.GetProtoNode()
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

    return self.is_set(linked_message, rule_obj)
