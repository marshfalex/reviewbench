# Excerpt of src/flask/cli.py from an upstream project; code outside the functions below is omitted.
import ast
import inspect
import os
import platform
import re
import sys
import traceback
import warnings
from functools import update_wrapper
from operator import attrgetter
from threading import Lock
from threading import Thread
import click
from werkzeug.utils import import_string
from .globals import current_app
from .helpers import get_debug_flag
from .helpers import get_env
from .helpers import get_load_dotenv



def locate_app(script_info, module_name, app_name, raise_if_not_found=True):
    __traceback_hide__ = True  # noqa: F841

    try:
        __import__(module_name)
    except ImportError as e:
        # Reraise the ImportError if it occurred within the imported module.
        # Determine this by checking whether the trace has a depth > 1.
        if sys.exc_info()[2].tb_next:
            raise NoAppException(
                f"While importing {module_name!r}, an ImportError was raised."
            ) from e
        elif raise_if_not_found:
            raise NoAppException(f"Could not import {module_name!r}.") from e
        else:
            return

    module = sys.modules[module_name]

    if app_name is None:
        return find_best_app(script_info, module)
    else:
        return find_app_by_string(script_info, module, app_name)
