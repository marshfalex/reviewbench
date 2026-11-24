# Excerpt of src/click/core.py from an upstream project; code outside the functions below is omitted.
import enum
import errno
import os
import sys
import typing as t
from contextlib import contextmanager
from contextlib import ExitStack
from functools import update_wrapper
from gettext import gettext as _
from gettext import ngettext
from itertools import repeat
from ._unicodefun import _verify_python_env
from .exceptions import Abort
from .exceptions import BadParameter
from .exceptions import ClickException
from .exceptions import Exit
from .exceptions import MissingParameter
from .exceptions import UsageError
from .formatting import HelpFormatter
from .formatting import join_options
from .globals import pop_context
from .globals import push_context
from .parser import _flag_needs_value
from .parser import OptionParser
from .parser import split_opt
from .termui import confirm
from .termui import prompt
from .termui import style
from .types import _NumberRangeBase
from .types import BOOL
from .types import convert_type
from .types import IntRange
from .utils import _detect_program_name
from .utils import _expand_args
from .utils import echo
from .utils import make_default_short_help
from .utils import make_str
from .utils import PacifyFlushWrapper



class Context:
    # [... omitted ...]

    def invoke(*args, **kwargs):  # noqa: B902
        """Invokes a command callback in exactly the way it expects.  There
        are two ways to invoke this method:

        1.  the first argument can be a callback and all other arguments and
            keyword arguments are forwarded directly to the function.
        2.  the first argument is a click command object.  In that case all
            arguments are forwarded as well but proper click parameters
            (options and click arguments) must be keyword arguments and Click
            will fill in defaults.

        Note that before Click 3.2 keyword arguments were not properly filled
        in against the intention of this code and no context was created.  For
        more information about this change and why it was done in a bugfix
        release see :ref:`upgrade-to-3.2`.
        """
        self, callback = args[:2]
        ctx = self

        # It's also possible to invoke another command which might or
        # might not have a callback.  In that case we also fill
        # in defaults and make a new context for this command.
        if isinstance(callback, Command):
            other_cmd = callback
            callback = other_cmd.callback

            if callback is None:
                raise TypeError(
                    "The given command does not have a callback that can be invoked."
                )

            ctx = self._make_sub_context(other_cmd)

            for param in other_cmd.params:
                if param.name not in kwargs and param.expose_value:
                    kwargs[param.name] = param.get_default(ctx)

        args = args[2:]
        with augment_usage_errors(self):
            with ctx:
                return callback(*args, **kwargs)

    def forward(*args, **kwargs):  # noqa: B902
        """Similar to :meth:`invoke` but fills in default keyword
        arguments from the current context if the other command expects
        it.  This cannot invoke callbacks directly, only other commands.
        """
        self, cmd = args[:2]

        # Can only forward to other commands, not direct callbacks.
        if not isinstance(cmd, Command):
            raise TypeError("Callback is not a command.")

        for param in self.params:
            if param not in kwargs:
                kwargs[param] = self.params[param]

        return self.invoke(cmd, **kwargs)
