# Excerpt of rich/color.py from an upstream project; code outside the functions below is omitted.
import platform
import re
from colorsys import rgb_to_hls
from enum import IntEnum
from functools import lru_cache
from typing import TYPE_CHECKING, NamedTuple, Optional, Tuple
from ._palettes import EIGHT_BIT_PALETTE, STANDARD_PALETTE, WINDOWS_PALETTE
from .color_triplet import ColorTriplet
from .repr import Result, rich_repr
from .terminal_theme import DEFAULT_TERMINAL_THEME



class Color:
    # [... omitted ...]

    @lru_cache(maxsize=1024)
    def downgrade(self, system: ColorSystem) -> "Color":
        """Downgrade a color system to a system with fewer colors."""

        if self.type in (ColorType.DEFAULT, system):
            return self
        # Convert to 8-bit color from truecolor color
        if system == ColorSystem.EIGHT_BIT and self.system == ColorSystem.TRUECOLOR:
            assert self.triplet is not None
            red, green, blue = self.triplet.normalized
            _h, l, s = rgb_to_hls(red, green, blue)
            # If saturation is under 10% assume it is grayscale
            if s < 0.1:
                gray = round(l * 25.0)
                if gray == 0:
                    color_number = 16
                elif gray == 25:
                    color_number = 231
                else:
                    color_number = 231 + gray
                return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

            color_number = (
                16 + 36 * round(red * 5.0) + 6 * round(green * 5.0) + round(blue * 5.0)
            )
            return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

        # Convert to standard from truecolor or 8-bit
        elif system == ColorSystem.STANDARD:
            if self.system == ColorSystem.TRUECOLOR:
                assert self.triplet is not None
                triplet = self.triplet
            else:  # self.system == ColorSystem.EIGHT_BIT
                assert self.number is not None
                triplet = ColorTriplet(*EIGHT_BIT_PALETTE[self.number])

            color_number = STANDARD_PALETTE.match(triplet)
            return Color(self.name, ColorType.STANDARD, number=color_number)

        elif system == ColorSystem.WINDOWS:
            if self.system == ColorSystem.TRUECOLOR:
                assert self.triplet is not None
                triplet = self.triplet
            else:  # self.system == ColorSystem.EIGHT_BIT
                assert self.number is not None
                if self.number < 16:
                    return Color(self.name, ColorType.WINDOWS, number=self.number)
                triplet = ColorTriplet(*EIGHT_BIT_PALETTE[self.number])

            color_number = WINDOWS_PALETTE.match(triplet)
            return Color(self.name, ColorType.WINDOWS, number=color_number)

        return self
