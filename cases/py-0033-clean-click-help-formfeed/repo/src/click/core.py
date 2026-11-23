# Excerpt of click's src/click/core.py; unrelated code is omitted.
import inspect
import os

from .formatting import HelpFormatter
from .globals import _


class Command:
    # [... omitted ...]

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        """Writes the help text to the formatter if it exists."""
        text = self.help if self.help is not None else ""

        if self.deprecated:
            text = _("(Deprecated) {text}").format(text=text)

        if text:
            text = inspect.cleandoc(text).partition("\f")[0]
            formatter.write_paragraph()

            with formatter.indentation():
                formatter.write_text(text)
