# Excerpt of src/click/termui.py from an upstream project; code outside the functions below is omitted.
import inspect
import io
import itertools
import os
import sys
import typing as t
from ._compat import is_bytes
from ._compat import isatty
from ._compat import strip_ansi
from ._compat import WIN
from .exceptions import Abort
from .exceptions import UsageError
from .globals import resolve_color_default
from .types import Choice
from .types import convert_type
from .utils import echo
from .utils import LazyFile



def confirm(
    text, default=False, abort=False, prompt_suffix=": ", show_default=True, err=False
):
    """Prompts for confirmation (yes/no question).

    If the user aborts the input by sending a interrupt signal this
    function will catch it and raise a :exc:`Abort` exception.

    .. versionadded:: 4.0
       Added the `err` parameter.

    :param text: the question to ask.
    :param default: the default for the prompt.
    :param abort: if this is set to `True` a negative answer aborts the
                  exception by raising :exc:`Abort`.
    :param prompt_suffix: a suffix that should be added to the prompt.
    :param show_default: shows or hides the default value in the prompt.
    :param err: if set to true the file defaults to ``stderr`` instead of
                ``stdout``, the same as with echo.
    """
    prompt = _build_prompt(
        text, prompt_suffix, show_default, "Y/n" if default else "y/N"
    )
    while 1:
        try:
            # Write the prompt separately so that we get nice
            # coloring through colorama on Windows
            echo(prompt, nl=False, err=err)
            value = visible_prompt_func("").lower().strip()
        except (KeyboardInterrupt, EOFError):
            raise Abort()
        if value in ("y", "yes"):
            rv = True
        elif value in ("n", "no"):
            rv = False
        elif value == "":
            rv = default
        else:
            echo("Error: invalid input", err=err)
            continue
        break
    if abort and not rv:
        raise Abort()
    return rv
