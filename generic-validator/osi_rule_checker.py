from iso3166 import countries
from protobuf_to_dict import protobuf_to_dict
from copy import deepcopy
from importlib import reload


class OsiRuleChecker:

    def __init__(self, logger, id_manager):
        self._rules = dict()
        self._logger = logger
        self._id_manager = id_manager

    # Rules implementation
    def is_set(self, inherit, rules, params):
        if hasattr(inherit[-1][1], "DESCRIPTOR"):
            return self.is_valid(inherit, rules, params)
        else:
            return True

    def is_set_if(self, inherit, rules, params):
        return self.is_set(inherit, rules, params)

    def is_valid(self, inherit, rules, params):
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

    def is_minimum(self, inherit, rules, minimum):
        self._logger.debug(f'Minimum: {minimum}')
        value = inherit[-1][1]
        res = value >= minimum
        if not res:
            self._logger.error(f'{get_message_path(inherit)} = {value} is too low (minimum: {minimum})')
        return res

    def is_maximum(self, inherit, rules, maximum):
        self._logger.debug(f'Maximum: {maximum}')
        value = inherit[-1][1]
        res = value >= maximum
        if not res:
            self._logger.error(f'{get_message_path(inherit)} = {value} is too high (maximum: {maximum})')
        return res

    def in_range(self, inherit, rules, range):
        m = float(range[0])
        M = float(range[1])
        v = inherit[-1][1]
        message_ok = f'{get_message_path(inherit)} = {v} in range: {m, M}'
        message_nok = f'{get_message_path(inherit)} = {v} not in range: {m, M}'
        if m <= v and v <= M:
            # range is left open
            if len(range) >= 3 and str.find(range[2], 'lo') >= 0 and m == v:
                self._logger.debug(message_ok)
                return False
            # range is right open
            elif len(range) >= 3 and str.find(range[2], 'ro') >= 0 and M == v:
                self._logger.debug(message_ok)
                return False
            else:
                self._logger.debug(message_nok)
                return True
        else:
            self._logger.error(message_ok)
            return False

    def is_global_unique(self, inherit, rules, params):
        """
        Must be set to an Identifier
        """
        object_of_id = inherit[-2][1]
        identifier = inherit[-1][1].value

        return self._id_manager.register_message(identifier, object_of_id)

    def refers(self, inherit, rules, params):
        referer = inherit[-2][1]
        identifier = inherit[-1][1].value
        expected_type = params
        condition = None  # TODO
        self._id_manager.refer(referer, identifier, expected_type, condition)
        return True

    def is_iso_country_code(self, inherit, rules, params):
        self._logger.debug(f'Checking ISO code for {inherit[-1][1]}')
        iso_code = inherit[-1][1]
        try:
            countries.get(iso_code)
            self._logger.debug(f'ISO code {iso_code} is valid')
            return True
        except KeyError:
            self._logger.debug(f'ISO code {iso_code} is not valid')
            return False

    def first_element(self, inherit, rules, params):
        r = self.check_message(inherit + [(None, inherit[-1][1][0])], params)
        return r

    def last_element(self, inherit, rules, params):
        return self.check_message(inherit + [(None, inherit[-1][1][-1])], params)

    def _has_attr(self, message, field_name):
        try:
            return message.HasField(field_name)
        except ValueError:
            try:
                return len(getattr(message, field_name)) > 0
            except AttributeError:
                return False

    def _check_repeated(self, rule_method, inherit, rules, params):
        self._logger.debug(
            f'Check the rule {rule_method.__name__} for a repeated field')

        if rule_method.__name__ == "each":
            rules = params
        if rule_method.__name__ in ['first_element', 'last_element']:
            return rule_method(inherit, rules, params)
        else:
            return all([rule_method(inherit + [(None, m)], rules, params) for m in inherit[-1][1]])

    def check_message(self, inherit, rules):
        """Method to check the rules for a complex message
        It is also the input method

        Keyword arguments:
        inherit --  a list representing the inheritance of the processed message in tuples like this:
                    [(None, Root message), (Field descriptor, Child message), etc.]
                    The last tuple represent the processed message
        rules   --  the dictionary for the rules rooted at the type of the processed message
        """
        final_res = True
        # Add "is_valid" rule for each field that can be validated (default)
        message = inherit[-1][1]
        for desc, _ in filter(lambda m: m[0].message_type is not None, message.ListFields()):
            if desc.name not in rules:
                rules[desc.name] = ['is_valid']
            elif not('is_valid' in rules[desc.name] or 'is_set' in rules[desc.name]):
                rules[desc.name].append('is_valid')

        proto_field_tuples = message.ListFields()
        inherit_message_t = get_message_path(inherit)

        # loop over the fields in the rules
        for field_name, field_rules in rules.items():

            # check the rule "is_set"
            if field_rules is None:
                continue
            if "is_set" in field_rules and self._has_attr(message, field_name):
                self._logger.debug(
                    f'{inherit_message_t}.{field_name} is set as expected')
            elif "is_set" in field_rules:
                self._logger.error(
                    f'{inherit_message_t}.{field_name} is not set!')
                continue

            # "is_set_if" is the conditional version of the rule "is_set"
            # check if the rule exists for an attribute
            is_set_if_rule = {"is_set_if": d['is_set_if'] for d in filter(
                lambda d: type(d) == dict and 'is_set_if' in d, field_rules)}

            if len(is_set_if_rule) >= 1:
                cond = is_set_if_rule['is_set_if']

                dict_message = protobuf_to_dict(message)
                result = eval(cond, dict_message)
                field_is_set = self._has_attr(message, field_name)
                if result and field_is_set:
                    self._logger.debug(
                        f'{inherit_message_t}.{field_name} is set as expected: {cond}')
                elif result and not field_is_set:
                    self._logger.error(
                        f'{inherit_message_t}.{field_name} is not set as expected: {cond}')

            # if the name starts with an upper char, it is a submessage type
            if field_name[0].isupper():
                continue

            try:
                proto_field_tuple = next(
                    filter(lambda t: t[0].name == field_name, proto_field_tuples))
            except StopIteration:
                self._logger.debug(
                    f'Field {inherit_message_t}.{field_name} does not exist')
            else:
                # loop over the rules of one field
                for rule in field_rules:
                    if len(rule) == 1 and type(rule) is str:
                        self._logger.exception(
                            f'''Error in the rules file for {message.DESCRIPTOR.name}:
                            each element of a list of rules for an attribute must be preceded
                            by an hyphen "-"''')

                    verb, params = parse_yaml_rule(rule)

                    try:
                        rule_checker = getattr(self, verb)
                    except AttributeError:
                        self._logger.error(
                            f'Rule "{verb}" not implemented yet!')
                    else:
                        child_inherit = inherit + \
                            [next(filter(lambda t: t[0].name ==
                                         field_name, proto_field_tuples))]

                        # If the field is "REPEATED"
                        if proto_field_tuple[0].label == 3:
                            res = self._check_repeated(
                                rule_checker, child_inherit, rules, params)
                        else:
                            res = rule_checker(child_inherit,
                                               rules, params)

                        if not(res):
                            final_res = False
        return final_res

def parse_yaml_rule(rule):
    """Check if the rule has parameters or not
    if there is a column, YAML parses it as a dict
    """
    if type(rule) is dict:
        verb, params = next(iter(rule.items()))
    else:
        verb, params = rule, []

    return verb, params

def get_message_path(inherit):
    return ".".join(map(lambda i: i[0].name, filter(lambda i: i[0] is not None, inherit)))
