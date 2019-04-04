import logging

class OSIValidatorLogger(logging.Logger):

    def __init__(self, *args):
        self.warning_messages = []
        self.debug_messages = []
        self.error_messages = []

        super().__init__(*args)
        self.setLevel(10)
    
    def debug(self, msg, *args, **kwargs):
        self.debug_messages.append(msg)
        return super().debug(msg, *args, **kwargs)
        
    def warning(self, msg, *args, **kwargs):
        self.warning_messages.append(msg)
        return super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.error_messages.append(msg)
        return super().error(msg, *args, **kwargs)

    def flush(self):
        print(f"Warnings ({len(self.warning_messages)})")
        for warning_message in self.warning_messages:
            print(warning_message)
        self.warning_messages = []
        print()
            
        print(f"Errors ({len(self.error_messages)})")
        for error_message in self.error_messages:
            print(error_message)

        self.error_messages = []