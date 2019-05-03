from copy import deepcopy
from iso3166 import countries
from protobuf_to_dict import protobuf_to_dict
from asteval import Interpreter
from osi_validation_rules import Severity, MessageType
from osi_validator_logger import SEVERITY

class OSIRuleChecker:
    """This class contains all the available rules to write OSI requirements and
    the necessary methods to check their compliance.
    """

    def __init__(self, ovr, logger, id_manager):
        self._rules = ovr.t_rules
        self._logger = logger
        self._id_manager = id_manager

    # Rules implementation
    def is_set(self, timestep, severity, inherit, *args):
        """Check if a field is set. The Python function is actually a wrapper of
        is_valid.
        The setting of the field is checked during the exploration of the
        fields.

        :param params: ignored
        """
        if hasattr(inherit[-1][1], "DESCRIPTOR"):
            return self.is_valid(timestep, severity, inherit, *args)
        return True

    def is_set_if(self, timestep, severity, inherit, *args):
        """A wrapper to the function is_set. The condition should be contained
        in "params" as a string but is checked during the exploration of the
        message.
        """
        return self.is_set(timestep, severity, inherit, *args)

    def is_valid(self, timestep, _severity, inherit, *_):
        """Check if a field message is valid, that is all the inner rules of the
        message in the field are complying.

        :param params: ignored
        """
        field = inherit[-1][1]

        field_type_desc = field.DESCRIPTOR
        message_t_inherit = []
        while field_type_desc is not None:
            message_t_inherit.insert(0, field_type_desc.name)
            field_type_desc = field_type_desc.containing_type

        return self.check_message(timestep, inherit,
                                  self._rules.get_type(message_t_inherit))

    def is_minimum(self, timestep, severity, inherit, _, minimum):
        """Check if a number is over a minimum.

        :param minimum: the minimum
        """
        self._logger.debug(timestep, f'Minimum: {minimum}')
        value = inherit[-1][1]
        res = value >= minimum
        if not res:
            self._log(timestep, severity,
                      f'{get_message_path(inherit)} = {value} is too low '+\
                      f'(minimum: {minimum})')
        return res

    def is_maximum(self, timestep, severity, inherit, _, maximum):
        """Check if a number is under a maximum.

        :param maximum: the maximum
        """
        self._logger.debug(timestep, f'Maximum: {maximum}')
        value = inherit[-1][1]
        res = value >= maximum
        if not res:
            self._log(timestep, severity,
                      f'{get_message_path(inherit)} = {value} is too high '+\
                      f'(maximum: {maximum})')
        return res

    def in_range(self, timestep, severity, inherit, _, interval):
        """Check if a number is in a range.

        :param range: must be a table. The first element is the minimum, the
                      second element is the maximum. The first element, if
                      present, is a parameter string:

                      - if it contains 'lo', the interval is left-open
                      - if it contains 'ro', the interval is right-open

                      The interval can be 'loro', that is left and right-open.
        """
        mini = float(interval[0])
        maxi = float(interval[1])
        value = inherit[-1][1]

        result = mini <= value <= maxi and not(
            len(interval) >= 3 and (
                (str.find(interval[2], 'lo') >= 0  # range is left open
                 and mini == value)
                or (str.find(interval[2], 'ro') >= 0  # range is right open
                    and maxi == value))
        )

        n_in = "not " if not result else ""

        message_model = \
            f'{get_message_path(inherit)}= {value} {n_in}in range: {mini, maxi}'

        log_severity = "debug" if result else severity
        self._log(timestep, log_severity, message_model)
        return result

    def is_global_unique(self, timestep, _severity, inherit, *_):
        """Register an ID in the OSI ID manager to later perform a ID
        consistency validation.

        Must be set to an Identifier.

        :param params: ignored
        """
        object_of_id = inherit[-2][1]
        identifier = inherit[-1][1].value

        return self._id_manager.register_message(identifier, object_of_id)

    def refers(self, timestep, _severity, inherit, _, params):
        """Add a reference to another message by ID.

        TODO: the conditional reference. Still no case of use in OSI let this
        pending.

        :param params: id of the refered object
        """
        referer = inherit[-2][1]
        identifier = inherit[-1][1].value
        expected_type = params
        condition = None # TODO
        self._id_manager.refer(referer, identifier, expected_type, condition)
        return True

    def is_iso_country_code(self, timestep, severity, inherit, *_):
        """Check if a string is a ISO country code.

        :param params: string to be checked
        """
        self._logger.debug(timestep, f'Checking ISO code for {inherit[-1][1]}')
        iso_code = inherit[-1][1]
        try:
            countries.get(iso_code)
            self._logger.debug(timestep, f'ISO code {iso_code} is valid')
            return True
        except KeyError:
            self._log(timestep, severity, f'ISO code {iso_code} is not valid')
            return False

    def first_element(self, timestep, _severity, inherit, _, params):
        """Check rule for first message of a repeated field.

        :param params: dictionary of rules to be checked for the first message
        """
        virtual_message = MessageType('', params)
        return self.check_message(
            timestep, inherit + [(None, inherit[-1][1][0])], virtual_message)

    def last_element(self, timestep, _severity, inherit, _, params):
        """Check rule for last message of a repeated field.

        :param params: dictionary of rules to be checked for the last message
        """
        virtual_message = MessageType('', params)
        return self.check_message(
            timestep, inherit + [(None, inherit[-1][1][-1])], virtual_message)

    def _check_repeated(self, timestep, severity, rule_method, inherit, rules,
                        params):
        self._logger.debug(
            timestep,
            f'Check the rule {rule_method.__name__} for a repeated field')

        if rule_method.__name__ == "each":
            rules = params
        if rule_method.__name__ in ['first_element', 'last_element']:
            return rule_method(timestep, severity, inherit, rules, params)
        else:
            return all([rule_method(timestep, severity, inherit + [(None, m)],
                                    rules, params)
                        for m in inherit[-1][1]])

    def check_message(self, timestep, inherit, rules):
        """Method to check the rules for a complex message
        It is also the input method

        :param inherit: a list representing the inheritance of the processed
                        message in tuples
        :param rules: the dictionary for the rules rooted at the type of the
                      processed message

        .. note:: inherit parameter must have this structure:
                  ``[(None, Root message), (Field descriptor, Child message),
                  etc.]``

                  The last tuple represents the processed message.
        """
        final_res = True
        # Add "is_valid" rule for each field that can be validated (default)
        message = inherit[-1][1]

        add_default_valid_rules(message, rules)

        # loop over the fields in the rules where field are set
        # if the name starts with an upper char, it is a submessage type
        for field_name, f_rules in rules.fields.items():

            field_path = get_message_path(inherit) + "." + field_name

            # check the rule "is_set"
            if f_rules.must_be_set:
                if has_attr(message, field_name):
                    self._logger.debug(
                        timestep, f'{field_path} is set as expected')
                else:
                    self._log(timestep, f_rules.rules['is_set'].severity,
                              f"{field_path} is not set!")
                    continue

            # "is_set_if" is the conditional version of the rule "is_set"
            # check if the rule exists for an attribute
            if f_rules.must_be_set_if is not None:
                cond = f_rules.must_be_set_if
                cond_check = Interpreter(protobuf_to_dict(message))(cond)
                if cond_check:
                    if has_attr(message, field_name):
                        self._logger.debug(
                            timestep, f"{field_path} set as expected: {cond}")
                    else:
                        self._log(timestep, f_rules.rules['is_set_if'].severity,
                                  f"{field_path} not set as expected: {cond}")
                else:
                    self._logger.debug(
                        timestep, f"{field_path}: {cond} not fulfilled")

            try:
                proto_field_tuple = next(
                    filter(lambda t, fn=field_name: t[0].name == fn,
                           message.ListFields()))
                child_inherit = inherit + [proto_field_tuple]
            except StopIteration:
                self._logger.debug(timestep,
                                   f'Field {field_path} does not exist')
            else: # if the field exists
                # loop over the rules of one field
                res = self._loop_over_rules(timestep, rules, f_rules,
                                            child_inherit)

                final_res = False if not res else final_res
        return final_res

    def _loop_over_rules(self, timestep, rules, field_rules, child_inherit):
        final_res = True
        for _, rule_obj in field_rules.rules.items():
            verb = rule_obj.verb
            params = rule_obj.params
            severity = SEVERITY[rule_obj.severity]

            try:
                rule_checker = getattr(self, verb)
            except AttributeError:
                self._logger.error(timestep,
                                   f'Rule "{verb}" not implemented yet!')
            else:
                # If the field is "REPEATED"
                if child_inherit[-1][0].label == 3:
                    res = self._check_repeated(
                        timestep, severity, rule_checker, child_inherit, rules,
                        params)
                else:
                    res = rule_checker(timestep, severity, child_inherit, rules,
                                       params)

                final_res = False if not res else final_res
        return final_res

    def _log(self, timestep, severity, message):
        if isinstance(severity, Severity):
            severity_method = SEVERITY[severity]
        elif isinstance(severity, str):
            severity_method = severity
        else:
            raise TypeError('type not accepted: must be Severity enum or str')

        return getattr(self._logger, severity_method)(timestep, message)

def get_message_path(inherit):
    """Return the path to a message from the inheritance list of the message.
    """
    not_none_elt = filter(lambda i: i[0] is not None, inherit)
    return ".".join(map(lambda i: i[0].name, not_none_elt))


def has_attr(message, field_name):
    """Check if a message have an attribute/field even if this is a repeated
    field.
    """
    try:
        return message.HasField(field_name)
    except ValueError:
        try:
            return len(getattr(message, field_name)) > 0
        except AttributeError:
            return False

def add_default_valid_rules(message, rules):
    """Add "is_valid" rule to all the field of message without is_set or
    is_valid
    """
    def is_validable(message):
        return message[0].message_type is not None
    for desc, _ in filter(is_validable, message.ListFields()):
        if desc.name not in rules.fields:
            rules.add_field(desc.name)
            rules[desc.name].add_rule('is_valid')
        elif not rules.fields[desc.name].must_be_set:
            rules[desc.name].add_rule('is_valid')
