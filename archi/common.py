import logging
import functools
mlogger = logging.getLogger('archi-external-use.parsexml')

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mlogger.debug(f'Start of the function {func.__name__}')
        response = func(*args, **kwargs)
        mlogger.debug(f'End of the function {func.__name__}')
        return response
    return wrapper