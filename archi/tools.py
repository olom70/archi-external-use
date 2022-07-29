import os
import logging
import functools
from xml.dom import minidom

mlogger = logging.getLogger('archi-external-use.tools')

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mlogger.info(f'Start of the function {func.__name__}')
        response = func(*args, **kwargs)
        mlogger.info(f'End of the function {func.__name__}')
        return response
    return wrapper



@log_function_call
def read_model(fileToRead: str) -> tuple:
    '''
        Read an archimate model (in "open exchange" format) and put
        all elements, relationships in lists
    '''
    elements = []
    elementsNames = []
    elementsDocumentation = []
    elementsProperties = []

    try:
        with open(fileToRead, encoding='utf-8') as xmltoanalyse:
            dom = minidom.parse(xmltoanalyse)
        


        return elements, elementsNames, elementsDocumentation, elementsProperties
    except BaseException as be:
        mlogger.critical(f'Unknown error in function read_model : {type(be)}{be.args}')
        return None, None, None, None

