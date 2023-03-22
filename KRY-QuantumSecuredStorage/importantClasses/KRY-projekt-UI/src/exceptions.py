from src.utilities import log_print

class KRYException(Exception):
    """ Neat way of printing and logging exceptions """
    def __init__(self, message):
        """ docstring """
        super().__init__()
        log_print(message)


class OptionException(KRYException):
    """ child """
    pass
