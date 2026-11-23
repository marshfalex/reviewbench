# Excerpt of click's src/click/core.py; unrelated code is omitted.
import inspect
import os

from .formatting import HelpFormatter
from .globals import _


class BaseCommand:
    # [... omitted ...]

    def _main_shell_completion(
        self,
        ctx_args: t.MutableMapping[str, t.Any],
        prog_name: str,
        complete_var: t.Optional[str] = None,
    ) -> None:
        """Check if the shell is asking for tab completion, process
        that, then exit early. Called from :meth:`main` before the
        program is invoked.

        :param prog_name: Name of the executable in the shell.
        :param complete_var: Name of the environment variable that holds
            the completion instruction. Defaults to
            ``_{PROG_NAME}_COMPLETE``.
        """
        if complete_var is None:
            complete_var = f"_{prog_name}_COMPLETE".replace("-", "_").upper()

        instruction = os.environ.get(complete_var)

        if not instruction:
            return

        from .shell_completion import shell_complete

        rv = shell_complete(self, ctx_args, prog_name, complete_var, instruction)
        sys.exit(rv)
