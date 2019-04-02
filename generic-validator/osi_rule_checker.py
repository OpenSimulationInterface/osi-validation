import logging
from iso3166 import countries
from protobuf_to_dict import protobuf_to_dict

class OsiRuleChecker:

    def __init__(self):
        self._rules = dict()
        self._identifiers = dict()
        self._object_tree = dict()
        self._references = dict()
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Rules implementation
    def is_set(self, inherit, rules, params):
        if hasattr(inherit[-1][1], "DESCRIPTOR"):
            return self.is_valid(inherit, rules, params)
        else:
            return True

    def is_set_if(self, inherit, rules, params):
        return True

    def is_valid(self, inherit, rules, params):
        field = inherit[-1][1]
        containing_type_desc = field.DESCRIPTOR.containing_type
        field_type_desc = field.DESCRIPTOR
        contained_rules = {}
        try:
            if containing_type_desc is not None:
                contained_rules = rules[field_type_desc.name]
                logging.debug(f'Contained type!')
            else:
                contained_rules = self._rules[field_type_desc.name]
        except KeyError:
            logging.warning(
                f'The message type \'{field_type_desc.name}\' has no rule')
            return True
        else:
            return self.check_message(inherit, contained_rules)

    def _check_repeated(self, rule_method, inherit, rules, params):
        logging.debug(
            f'Check the rule {rule_method.__name__} for a repeated field')
        return all([rule_method(inherit + [(None, m)], rules, params) for m in inherit[-1][1]])

    def is_minimum(self, inherit, rules, minimum):
        logging.debug(f'Minimum: {minimum}')
        return inherit[-1][1] >= minimum

    def is_maximum(self, inherit, rules, maximum):
        logging.debug(f'Maximum: {maximum}')
        return inherit[-1][1] <= maximum

    def in_range(self, inherit, rules, range):
        m = float(range[0])
        M = float(range[1])
        v = inherit[-1][1]
        if m <= v and v <= M:
            if len(range) >= 3 and str.find(range[2], 'lo') >= 0 and m == v:
                logging.debug(f'{v} not in range: {m, M}')
                return False
            elif len(range) >= 3 and str.find(range[2], 'ro') >= 0 and M == v:
                logging.debug(f'{v} not in range: {m, M}')
                return False
            else:
                logging.debug(f'{v} in range: {m, M}')
                return True
        else:
            logging.error(
                f'{v} not in range: {m, M}')
            return False

    def is_global_unique(self, inherit, rules, params):
        '''
        Must be set to an Identifier
        '''
        object_of_id = inherit[-2]
        identifier = inherit[-1][1].value
        if identifier in self._identifiers:
            logging.warning(f'The id {identifier} is already used')
            if type(inherit) in map(type, self._identifiers):
                logging.error(
                    f'Several {type(object_of_id)} have the id ({identifier})')
            self._identifiers[identifier].append(object_of_id)
            return False
        else:
            self._identifiers[identifier] = [object_of_id]
            return True

    def refers(self, inherit, rules, params):
        if params.startswith("$"):
            logging.debug('Check reference many to one')
            return params not in self._references or inherit[-1][1].value in self._references[params]
        if params.startswith("+"):
            logging.debug('Check reference many to many')
            try:
                return inherit[-1][1].value in self._references[params]
            except KeyError:
                logging.error('Reference error')
                return False

    def is_iso_country_code(self, inherit, rules, params):
        logging.debug(f'Checking ISO code for {inherit[-1][1]}')
        try:
            countries.get(inherit[-1][1])
            return True
        except KeyError:
            return False

    # Check launcher

    def check_message(self, inherit, rules):
        final_res = True
        # Add "is_valid" rule for each field that can be validated (default)
        message = inherit[-1][1]
        for desc, _ in filter(lambda m: m[0].message_type is not None, message.ListFields()):
            if desc.name not in rules:
                rules[desc.name] = ['is_valid']
            elif not('is_valid' in rules[desc.name] or 'is_set' in rules[desc.name]):
                rules[desc.name].append('is_valid')

        proto_field_tuples = message.ListFields()
        inherit_message_t = ".".join(map(lambda i: i[0].name, filter(
            lambda i: hasattr(i[1], "DESCRIPTOR") and i[0] is not None, inherit)))
        for field_name, field_rules in rules.items():
            if "is_set" in field_rules and message.HasField(field_name):
                logging.debug(
                    f'{inherit_message_t}.{field_name} is set as expected')
            elif "is_set" in field_rules:
                logging.error(f'{inherit_message_t}.{field_name} is not set!')
                continue

            is_set_if_rule = {"is_set_if": d['is_set_if'] for d in filter(
                lambda d: type(d) == dict and 'is_set_if' in d, field_rules)}
            if len(is_set_if_rule) >= 1:
                cond = is_set_if_rule['is_set_if']
                #logging.debug("is_set_if " + str(protobuf_to_dict(message)))
                result = eval(cond, protobuf_to_dict(message))
                try:
                    field_is_set = message.HasField(field_name)
                except ValueError:
                    field_is_set = len(getattr(message, field_name)) >= 0
                if result and field_is_set:
                    logging.debug(f'{inherit_message_t} is set as expected: {cond}')
                elif result and not field_is_set:
                    logging.error(f'{inherit_message_t} is not set as expected: {cond}')

            if field_name[0].isupper():
                continue

            try:
                proto_field_tuple = next(
                    filter(lambda t: t[0].name == field_name, proto_field_tuples))
            except StopIteration:
                logging.error(
                    f'Field {inherit_message_t}.{field_name} does not exist')
                logging.debug(list(map(lambda t: t[0].name, proto_field_tuples)))
            else:
                for rule in field_rules:
                    if len(rule) == 1 and type(rule) is str:
                        logging.exception(
                            f'''Error in the rules file for {message.DESCRIPTOR.name}:
                            each element of a list of rules for an attribute must be preceded
                            by an hyphen "-"''')

                    if type(rule) is dict:
                        verb, params = next(iter(rule.items()))
                    else:
                        verb, params = rule, []

                    try:
                        rule_checker = getattr(self, verb)
                    except AttributeError:
                        logging.error(f'Rule "{verb}" not implemented yet!')
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

                        if res:
                            logging.debug(
                                f'{verb} for {inherit_message_t}.{field_name} OK')
                        else:
                            logging.warning(
                                f'{verb} for {inherit_message_t}.{field_name} Not OK')
                            final_res = False
        return final_res
