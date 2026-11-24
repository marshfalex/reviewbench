# Excerpt of src/click/types.py from an upstream project; code outside the functions below is omitted.
import os
import stat
from datetime import datetime
from ._compat import _get_argv_encoding
from ._compat import filename_to_ui
from ._compat import get_filesystem_encoding
from ._compat import get_strerror
from ._compat import open_stream
from .exceptions import BadParameter
from .utils import LazyFile
from .utils import safecall



class Choice:
    # [... omitted ...]

    def shell_complete(self, ctx, param, incomplete):
        """Complete choices that start with the incomplete value.

        :param ctx: Invocation context for this command.
        :param param: The parameter that is requesting completion.
        :param incomplete: Value being completed. May be empty.

        .. versionadded:: 8.0
        """
        from click.shell_completion import CompletionItem

        str_choices = map(str, self.choices)
        return [CompletionItem(c) for c in str_choices if c.startswith(incomplete)]
