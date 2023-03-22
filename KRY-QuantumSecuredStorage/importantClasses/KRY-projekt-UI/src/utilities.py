import logging

def log_print(message, message_type="info", stdout=True):
    if stdout:
        print(message)
    
    func = logging.info
    if message_type == "info":
        func = logging.info
    elif message_type == "debug":
        func = logging.debug
    elif message_type == "warning":
        func = logging.warning
    elif message_type == "error":
        func = logging.error
    func(message)
