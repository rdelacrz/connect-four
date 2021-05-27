"""
Defines utility functions used by both the AI and the core logic.
"""

# Third-party modules
from cefpython3 import cefpython as cef

def js_callback(func):
    """
    Takes the return value of the function being wrapped and passes it through the callback function (if any).
    It is meant for JavaScript callback purposes, which cannot return a value because inter-process messaging 
    is asynchronous.
    """

    def wrapper(*args):
        # Grabs callback function from positional arguments (if one is provided)
        callback_fn = None
        func_args = args
        if type(args[-1]) is cef.JavascriptCallback:
            callback_fn = args[-1]
            func_args = args[:-1]

        # Passes return value from function accordingly (depending on whether a callback function is passed or not)
        ret = func(*func_args)
        if callback_fn is not None:
            callback_fn.Call(ret)
        else:
            return ret

    return wrapper