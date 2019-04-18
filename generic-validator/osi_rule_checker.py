from copy import deepcopy
from iso3166 import countries
from protobuf_to_dict import protobuf_to_dict

class OSIRuleChecker:

    def __init__(self, logger, id_manager):
        self._rules = dict()
        self._logger = logger
        self._id_manager = id_manager

    # Rules implementation
    def is_set(self, inherit, rules, params):
        """Check if a field is set. The Python function is actually a wrapper of
        is_valid.
        The setting of the field is checked during the exploration of the
        fields.

        :param params: ignored
        """
        if hasattr(inherit[-1][1], "DESCRIPTOR"):
            return self.is_valid(inherit, rules, params)
        return True

    def is_set_if(self, inherit, rules, params):
        """A wrapper to the function is_set. The condition should be contained
        in "params" as a string but is checked during the exploration of the
        message.
        """
        return self.is_set(inherit, rules, params)

    def is_valid(self, inherit, *_):
        """Check if a field message is valid, e.g. all the inner rules of the
        message in the field are complying.

        :param params: ignored
        """
        field = inherit[-1][1]

        field_type_desc = field.DESCRIPTOR
        contained_rules = deepcopy(self._rules)
        message_t_inherit = []
        while field_type_desc is not None:
            message_t_inherit.insert(0, field_type_desc.name)
            field_type_desc = field_type_desc.containing_type
        for i in message_t_inherit:
            contained_rules = contained_rules[i]

        return self.check_message(inherit, contained_rules)

    def is_minimum(self, inherit, _, minimum):
        """Check if a number is over a minimum.

        :param minimum: the minimum
        """
        self._logger.debug(f'Minimum: {minimum}')
        value = inherit[-1][1]
        res = value >= minimum
        if not res:
            self._logger.error(
                f'{get_message_path(inherit)} = {value} is too low (minimum: \
                    {minimum})')
        return res

    def is_maximum(self, inherit, _, maximum):
        """Check if a number is under a maximum.

        :param maximum: the maximum
        """
        self._logger.debug(f'Maximum: {maximum}')
        value = inherit[-1][1]
        res = value >= maximum
        if not res:
            self._logger.error(
                f'{get_message_path(inherit)} = {value} is too high (maximum: \
                    {maximum})')
        return res

    def in_range(self, inherit, _, interval):
        """Check if a number is in a range.

        :param range: must be a table. The first element is the minimum, the
                      second element is the maximum. The first element, if
                      present, is a parameter string:

                      - if it contains 'lo', the interval is left-open
                      - if it contains 'ro', the interval is right-open

                      The interval can be 'loro', e.g. left and right-open.
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

        self._logger.error(message_model)
        return result

    def is_global_unique(self, inherit, *_):
        """Register an ID in the OSI ID manager to later perform a ID
        consistency validation.

        Must be set to an Identifier.

        :param params: ignored
        """
        object_of_id = inherit[-2][1]
        identifier = inherit[-1][1].value

        return self._id_manager.register_message(identifier, object_of_id)

    def refers(self, inherit, _, params):
        """Add a reference to another message by ID.

        TODO: the conditional reference. Still no case of use in OSI let this
        pending.

        :param params: id of the refered object
        """
        referer = inherit[-2][1]
        identifier = inherit[-1][1].value
        expected_type = params
        condition = None  # TODO
        self._id_manager.refer(referer, identifier, expected_type, condition)
        return True

    def is_iso_country_code(self, inherit, *_):
        """Check if a string is a ISO country code.

        :param params: string to be checked
        """
        self._logger.debug(f'Checking ISO code for {inherit[-1][1]}')
        iso_code = inherit[-1][1]
        try:
            countries.get(iso_code)
            self._logger.debug(f'ISO code {iso_code} is valid')
            return True
        except KeyError:
            self._logger.debug(f'ISO code {iso_code} is not valid')
            return False

    def first_element(self, inherit, _, params):
        """Check rule for first message of a repeated field.

        :param params: dictionary of rules to be checked for the first message
        """
        return self.check_message(inherit + [(None, inherit[-1][1][0])], params)

    def last_element(self, inherit, _, params):
        """Check rule for last message of a repeated field.

        :param params: dictionary of rules to be checked for the last message
        """
        return self.check_message(inherit + [(None, inherit[-1][1][-1])],
                                  params)

    def _check_repeated(self, rule_method, inherit, rules, params):
        self._logger.debug(
            f'Check the rule {rule_method.__name__} for a repeated field')

        if rule_method.__name__ == "each":
            rules = params
        if rule_method.__name__ in ['first_element', 'last_element']:
            return rule_method(inherit, rules, params)
        else:
            return all([rule_method(inherit + [(None, m)], rules, params)
                        for m in inherit[-1][1]])

    def check_message(self, inherit, rules):
        """Method to check the rules for a complex message
        It is also the input method

        :param inherit: a list representing the inheritance of the processed
                        message in tuples
        :param rules: the dictionary for the rules rooted at the type of the
                      processed message

        .. note:: inherit parameter must have this structure:
                  ``[(None, Root message), (Field descriptor, Child message),
                  etc.]``

                  The last tuple represent the processed message.
        """
        final_res = True
        # Add "is_valid" rule for each field that can be validated (default)
        message = inherit[-1][1]

        add_default_valid_rules(message, rules)

        inherit_message_t = get_message_path(inherit)

        # loop over the fields in the rules where field are set
        # if the name starts with an upper char, it is a submessage type
        for field_name, field_rules \
            in {name: f_r for name, f_r in rules.items() \
                if f_r is not None and name[0].islower()}.items():

            # check the rule "is_set"
            if "is_set" in field_rules and has_attr(message, field_name):
                self._logger.debug(
                    f'{inherit_message_t}.{field_name} is set as expected')
            elif "is_set" in field_rules:
                self._logger.error(
                    f'{inherit_message_t}.{field_name} is not set!')
                continue

            # "is_set_if" is the conditional version of the rule "is_set"
            # check if the rule exists for an attribute
            is_set_if_rule = {
                "is_set_if": d['is_set_if'] for d in filter(
                    lambda d: isinstance(d, dict) and 'is_set_if' in d,
                    field_rules
                )}

            if len(is_set_if_rule) >= 1:
                cond = is_set_if_rule['is_set_if']

                if eval(cond, protobuf_to_dict(message), {}):
                    m_set = "is set as expected" \
                        if has_attr(message, field_name) \
                        else "is not set as expected"

                    self._logger.debug(
                        f'''{inherit_message_t}.{field_name} {m_set}: {cond}''')

            try:
                proto_field_tuple = next(
                    filter(lambda t, fn=field_name: t[0].name == fn,
                           message.ListFields()))
            except StopIteration:
                self._logger.debug(
                    f'Field {inherit_message_t}.{field_name} does not exist')
            else:
                # loop over the rules of one field
                for rule in field_rules:
                    # if len(rule) == 1 and isinstance(rule, str):
                    #     self._logger.exception(
                    #         f'''Error in the rules file for
                    #             {message.DESCRIPTOR.name}:
                    #         each element of a list of rules for an attribute
                    #         must be preceded by an hyphen "-"''')

                    verb, params = parse_yaml_rule(rule)

                    try:
                        rule_checker = getattr(self, verb)
                    except AttributeError:
                        self._logger.error(
                            f'Rule "{verb}" not implemented yet!')
                    else:
                        child_inherit = inherit + [proto_field_tuple]

                        # If the field is "REPEATED"
                        if proto_field_tuple[0].label == 3:
                            res = self._check_repeated(
                                rule_checker, child_inherit, rules, params)
                        else:
                            res = rule_checker(child_inherit,
                                               rules, params)

                        final_res = False if not res else final_res
        return final_res


def parse_yaml_rule(rule):
    """Check if the rule has parameters or not.

    If there is a column, YAML parses it as a dict.

    :return: Verb and list of param of the rule
    """
    if isinstance(rule, dict):
        verb, params = next(iter(rule.items()))
    else:
        verb, params = rule, []

    return verb, params


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
    validable_rules = filter(is_validable, message.ListFields())
    for desc, _ in validable_rules:
        if desc.name not in rules:
            rules[desc.name] = ['is_valid']
        else:
            try:
                next(filter(lambda e: e in ['is_valid', 'is_set'],
                            rules[desc.name]))
            except StopIteration:
                rules[desc.name].append('is_valid')
