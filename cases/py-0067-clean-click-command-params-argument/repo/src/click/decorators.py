# Excerpt of src/click/decorators.py from an upstream project; code outside the functions below is omitted.
import inspect
import types
import typing as t
from functools import update_wrapper
from gettext import gettext as _
from .core import Argument
from .core import Command
from .core import Context
from .core import Group
from .core import Option
from .core import Parameter
from .globals import get_current_context
from .utils import echo



def command(
    name: t.Union[str, t.Callable, None] = None,
    cls: t.Optional[t.Type[Command]] = None,
    **attrs: t.Any,
) -> t.Union[Command, t.Callable[[F], Command]]:
    r"""Creates a new :class:`Command` and uses the decorated function as
    callback.  This will also automatically attach all decorated
    :func:`option`\s and :func:`argument`\s as parameters to the command.

    The name of the command defaults to the name of the function with
    underscores replaced by dashes.  If you want to change that, you can
    pass the intended name as the first argument.

    All keyword arguments are forwarded to the underlying command class.

    Once decorated the function turns into a :class:`Command` instance
    that can be invoked as a command line utility or be attached to a
    command :class:`Group`.

    :param name: the name of the command.  This defaults to the function
                 name with underscores replaced by dashes.
    :param cls: the command class to instantiate.  This defaults to
                :class:`Command`.

    .. versionchanged:: 8.1
        This decorator can be applied without parentheses.
    """
    if cls is None:
        cls = Command

    func: t.Optional[t.Callable] = None

    if callable(name):
        func = name
        name = None

    def decorator(f: t.Callable[..., t.Any]) -> Command:
        if isinstance(f, Command):
            raise TypeError("Attempted to convert a callback into a command twice.")

        try:
            params = f.__click_params__  # type: ignore
        except AttributeError:
            params = []
        else:
            params.reverse()
            del f.__click_params__  # type: ignore

        if attrs.get("help") is None:
            attrs["help"] = f.__doc__

        cmd = cls(  # type: ignore[misc]
            name=name or f.__name__.lower().replace("_", "-"),  # type: ignore[arg-type]
            callback=f,
            params=params,
            **attrs,
        )
        cmd.__doc__ = f.__doc__
        return cmd

    if func is not None:
        return decorator(func)

    return decorator
