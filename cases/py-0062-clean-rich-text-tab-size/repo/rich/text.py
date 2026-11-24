# Excerpt of rich/text.py from an upstream project; code outside the functions below is omitted.
import re
from functools import partial, reduce
from math import gcd
from operator import itemgetter
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)
from ._loop import loop_last
from ._pick import pick_bool
from ._wrap import divide_line
from .align import AlignMethod
from .cells import cell_len, set_cell_size
from .containers import Lines
from .control import strip_control_codes
from .emoji import EmojiVariant
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import Style, StyleType



class Text:
    # [... omitted ...]

    def expand_tabs(self, tab_size: Optional[int] = None) -> None:
        """Converts tabs to spaces.

        Args:
            tab_size (int, optional): Size of tabs. Defaults to 8.

        """
        if "\t" not in self.plain:
            return
        if tab_size is None:
            tab_size = self.tab_size
        assert tab_size is not None
        result = self.blank_copy()

        new_text: List[Text] = []
        append = new_text.append

        for line in self.split("\n", include_separator=True):
            if "\t" not in line.plain:
                append(line)
            else:
                cell_position = 0
                parts = line.split("\t", include_separator=True)
                for part in parts:
                    if part.plain.endswith("\t"):
                        part._text[-1] = part._text[-1][:-1] + " "
                        cell_position += part.cell_len
                        tab_remainder = cell_position % tab_size
                        if tab_remainder:
                            spaces = tab_size - tab_remainder
                            part.extend_style(spaces)
                            cell_position += spaces
                    else:
                        cell_position += part.cell_len
                    append(part)

        result = Text("").join(new_text)

        self._text = [result.plain]
        self._length = len(self.plain)
        self._spans[:] = result._spans
