# Excerpt of jinja2/sandbox.py from an upstream project; code outside the functions below is omitted.
import types
import operator
from collections import Mapping
from jinja2.environment import Environment
from jinja2.exceptions import SecurityError
from jinja2._compat import string_types, PY2
from jinja2.utils import Markup
from markupsafe import EscapeFormatter
from string import Formatter
import warnings
from collections import deque
from collections import MutableSet, MutableMapping, MutableSequence



def inspect_format_method(callable):
    if not isinstance(callable, (types.MethodType,
                                 types.BuiltinMethodType)) or \
       callable.__name__ not in ('format', 'format_map'):
        return None
    obj = callable.__self__
    if isinstance(obj, string_types):
        return obj


class SandboxedEnvironment:
    # [... omitted ...]

    def format_string(self, s, args, kwargs, format_func=None):
        """If a format call is detected, then this is routed through this
        method so that our safety sandbox can be used for it.
        """
        if isinstance(s, Markup):
            formatter = SandboxedEscapeFormatter(self, s.escape)
        else:
            formatter = SandboxedFormatter(self)

        if format_func is not None and format_func.__name__ == 'format_map':
            if len(args) != 1 or kwargs:
                raise TypeError(
                    'format_map() takes exactly one argument %d given'
                    % (len(args) + (kwargs is not None))
                )

            kwargs = args[0]
            args = None

        kwargs = _MagicFormatMapping(args, kwargs)
        rv = formatter.vformat(s, args, kwargs)
        return type(s)(rv)

    def call(__self, __context, __obj, *args, **kwargs):
        """Call an object from sandboxed code."""
        fmt = inspect_format_method(__obj)
        if fmt is not None:
            return __self.format_string(fmt, args, kwargs, __obj)

        # the double prefixes are to avoid double keyword argument
        # errors when proxying the call.
        if not __self.is_safe_callable(__obj):
            raise SecurityError('%r is not safely callable' % (__obj,))
        return __context.call(__obj, *args, **kwargs)
