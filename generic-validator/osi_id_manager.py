class OSIIDManager:
    def __init__(self):
        self._index = dict()

    def _message_t_filter(self, message, message_t):
        if message_t is not None:
            return type(message) is message_t
        else:
            return True

    def get_all_messages_by_id(self, message_id, message_t=None):
        return list(filter(lambda m: self._message_t_filter(m, message_t), self._index[message_id]))

    def get_message_by_id(self, message_id, message_t=None):
        return next(filter(lambda m: self._message_t_filter(m, message_t), self._index[message_id]))

    def register_message(self, message_id, message):
        if message_id in self._index:
            self._index[message_id].append(message)
        else:
            self._index[message_id] = [message]
