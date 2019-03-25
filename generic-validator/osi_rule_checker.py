import logging


class OsiRuleChecker:

    def __init__(self):
        self._rules = dict()
        self._identifiers = dict()
        self._object_tree = dict()
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Rules implementation
    def is_valid(self, field, parent, rules):
        if not(hasattr(field, 'DESCRIPTOR')):
            return self._check_list(self.is_valid, field, parent, rules)

        logging.debug(f'Check the rule is_valid for {field.DESCRIPTOR.name}')
        containing_type = field.DESCRIPTOR.containing_type
        field_type = field.DESCRIPTOR.name
        contained_rules = {}
        try:
            if containing_type is not None and field_type in rules[containing_type]:
                contained_rules = rules[containing_type][field_type]
            else:
                contained_rules = self._rules[field.DESCRIPTOR.name]
        except KeyError:
            logging.warning(
                f'The message type \'{field_type}\' has no rule')
            return True
        else:
            return self.check_message(field, contained_rules)

    def _check_list(self, rule_method, list, *args):
        logging.debug(f'Check the rule {rule_method.__name__} for a list')
        return all([rule_method(message, *args) for message in list])

    def is_minimum(self, field, rules, parent, minimum):
        logging.debug(f'Check the rule is_minimum for {parent}')
        return field >= minimum

    def is_maximum(self, field, rules, parent, maximum):
        logging.debug(f'Check the rule is_maximum for {parent}')
        return field <= maximum

    def is_global_unique(self, field, parent, rules):
        '''
        Must be set to an Identifier
        '''
        logging.debug('Check the rule is_global_unique')

        identifier = field.value
        if identifier in self._identifiers:
            logging.warning(f'The id {identifier} is already used')
            if type(parent) in map(type, self._identifiers):
                logging.error(f'Two \'{parent}\' have the id {identifier}')
            self._identifiers[identifier].append(parent)
            return False
        else:
            self._identifiers[identifier] = [parent]
            return True

    # Check launcher

    def check_message(self, message, message_rules):
        for attr, attr_rules in message_rules.items():
            for rule in attr_rules:
                if len(rule) == 1 and type(rule) is str:
                    logging.exception(
                        f'Error in the rules file for {message.DESCRIPTOR.name}')
                field = getattr(message, attr)

                if type(rule) is dict:
                    verb, params = next(iter(rule.items()))
                else:
                    params = []
                    verb = rule
                rule_checker = getattr(self, verb)

                res = None
                try:
                    res = rule_checker(field, message, message_rules, *params)
                except TypeError:
                    res = rule_checker(field, message, message_rules, params)
                finally:
                    print(verb, res)
