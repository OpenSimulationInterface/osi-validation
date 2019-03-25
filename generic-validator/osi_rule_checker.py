import logging


class OsiRuleChecker:

    def __init__(self):
        self._rules = dict()
        self._identifiers = dict()
        self._object_tree = dict()
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Rules implementation
    def is_set(self, inheritance, rules, p):
        if hasattr(inheritance[-1], 'DESCRIPTOR'):
            return self.is_valid(inheritance, rules, p)

    def is_valid(self, inheritance, rules, p):
        if not(hasattr(inheritance[-1], 'DESCRIPTOR')):
            return self._check_repeated(self.is_valid, inheritance, rules, p)

        field = inheritance[-1]
        logging.debug(f'Check the rule is_valid for {field.DESCRIPTOR.name}')
        containing_type = field.DESCRIPTOR.containing_type
        field_type = field.DESCRIPTOR.name
        contained_rules = {}
        try:
            if containing_type is not None and field_type in rules[containing_type]:
                contained_rules = rules[containing_type][field_type]
                logging.debug(f'Contained type!')
            else:
                contained_rules = self._rules[field.DESCRIPTOR.name]
                logging.debug(f'Global type!')
        except KeyError:
            logging.warning(
                f'The message type \'{field_type}\' has no rule')
            return True
        else:
            return self.check_message(inheritance, contained_rules)

    def _check_repeated(self, rule_method, inheritance, rules, params):
        logging.debug(
            f'Check the rule {rule_method.__name__} for a list of {type(inheritance[-1][0])} in {type(inheritance[-2])}')
        return all([rule_method(inheritance + [message], rules, params) for message in inheritance[-1]])

    def is_minimum(self, inheritance, rules, minimum):
        return inheritance[-1] >= minimum

    def is_maximum(self, inheritance, rules, maximum):
        return inheritance[-1] <= maximum

    def is_global_unique(self, inheritance, rules, params):
        '''
        Must be set to an Identifier
        '''
        object_of_id = inheritance[-2]
        identifier = inheritance[-1].value
        if identifier in self._identifiers:
            logging.warning(f'The id {identifier} is already used')
            if type(inheritance) in map(type, self._identifiers):
                logging.error(
                    f'Two {type(object_of_id)} have the id ({identifier})')
            self._identifiers[identifier].append(object_of_id)
            return False
        else:
            logging.debug(f'ID ok!')
            self._identifiers[identifier] = [object_of_id]
            return True

    # Check launcher

    def check_message(self, inheritance, message_rules):
        # Add "is_valid" rule for each field that can be validated (default)
        message = inheritance[-1]
        for desc, value in filter(lambda m: m[0].message_type is not None, message.ListFields()):
            if desc.name not in message_rules:
                message_rules[desc.name] = ['is_valid']
            elif not('is_valid' in message_rules[desc.name] or 'is_set' in message_rules[desc.name]):
                message_rules[desc.name].append('is_valid')

        for field, field_rules in message_rules.items():
            for rule in field_rules:
                if len(rule) == 1 and type(rule) is str:
                    logging.exception(
                        f'Error in the rules file for {message.DESCRIPTOR.name}: each element of a list of rules for an attribut must be preceded by an hyphen "-"')

                if type(rule) is dict:
                    verb, params = next(iter(rule.items()))
                else:
                    params = []
                    verb = rule
                try:
                    rule_checker = getattr(self, verb)
                except AttributeError:
                    logging.error(f'Rule "{verb}" not implemented yet!')
                else:
                    if verb == "is_set" and message.HasField(field):
                        logging.debug(f'{field} is set as expected')
                    elif verb == "is_set":
                        logging.error(f'{field} is not set!')
                        continue

                    child_inheritance = inheritance + [getattr(message, field)]
                    logging.debug(
                        f'Check the rule {verb} for {list(map(type,child_inheritance))}')
                    res = rule_checker(child_inheritance,
                                       message_rules, params)
