from collections import Counter


class OSIIDManager:
    """Manage the ID of OSI Messages for verification of unicity and references
    """

    def __init__(self, logger):
        # id => [object1, object2...]
        # Each object (message) should have a different type
        # Ideally, there is only one object per id
        # to be resolved at the end
        self._index = dict()

        # [(referer_obj, id, expected_type, condition), ...]
        # one tuple per reference
        # to be resolved at the end
        self._references = []

        self.logger = logger

    def get_all_messages_by_id(self, message_id, message_t=None):
        """Retrieve all the message by giving an id"""
        return list(filter(lambda m: message_t_filter(m, message_t),
                           self._index[message_id]))

    def get_message_by_id(self, message_id, message_t=None):
        """Retrieve only one message by giving an id"""
        return next(filter(lambda m: message_t_filter(m, message_t),
                           self._index[message_id]))

    def register_message(self, message_id, message):
        """Register one message in the ID manager"""
        if message_id in self._index:
            self._index[message_id].append(message)
        else:
            self._index[message_id] = [message]
        return True

    def refer(self, referer, identifier, expected_type, condition=None):
        """Add a reference
        Condition is a function that will be applied on the found object if the
        reference is resolved
        """
        self._references.append(
            (referer, identifier, expected_type, condition))

    def resolve_unicity(self, timestamp):
        """Check for double ID"""
        for identifier, objects in self._index.items():
            types_counter = None
            if len(objects) > 1:
                types_list = list(map(type, objects))
                types_str_list = ", ".join(
                    map(lambda o: o.__name__, types_list))
                self.logger.warning(timestamp,
                                    f"Several objects of type " +
                                    f"{types_str_list} have the ID {identifier}"
                                    )

                if len(objects) != len(set(types_list)):
                    self.logger.error(timestamp,
                                      f"Several objects of the same type have" +
                                      f" the ID {identifier}:")
                    types_counter = Counter(list(types_list))
                    self.logger.error(
                        timestamp,
                        ", ".join(map(lambda t, tc=types_counter, i=identifier:
                                      f'{tc[t]} "{t.__name__}" have the ID {i}',
                                      filter(lambda t, tc=types_counter:
                                             tc[t] != 1,
                                             types_counter))))

    def resolve_references(self, timestamp):
        """Check if references are compliant"""
        for reference in self._references:
            _, identifier, expected_type, condition = reference
            try:
                found_object = next(filter(lambda o, et=expected_type: type(
                    o).__name__ == et, self._index[identifier]))
            except StopIteration:
                self.logger.error(
                    timestamp, f'Reference unresolved: {expected_type} ' +
                    f'(ID: {identifier})')
            else:
                self.logger.debug(
                    timestamp, f'Reference resolved: {expected_type} ' +
                    f'(ID: {identifier})')
                if condition is not None:
                    if condition(found_object):
                        self.logger.debug(timestamp, f'Condition OK')
                    else:
                        self.logger.error(timestamp, f'Condition not OK')

    def reset(self):
        """Erase all data in the ID manager"""
        self._index = {}
        self._references = []


def message_t_filter(message, message_t):
    """Check if a message is of type message_t"""
    if message_t is not None:
        return isinstance(message, message_t)
    return True
