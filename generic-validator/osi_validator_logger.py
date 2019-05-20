import logging

class OSIValidatorLogger(logging.Logger):

    warn = []
    
    def debug(self, msg, *args, **kwargs):
        return super().debug(msg, *args, **kwargs)
        
    def warning(self, msg, *args, **kwargs):

        return super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):


        return super().error(msg, *args, **kwargs)