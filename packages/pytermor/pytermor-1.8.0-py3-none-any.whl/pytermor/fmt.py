# -----------------------------------------------------------------------------
# pytermor [ANSI formatted terminal output toolset]
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
from __future__ import annotations

from typing import Any

from . import build, sgr, seq, SequenceSGR
from .registry import sgr_parity_registry


# noinspection PyMethodMayBeStatic
class Format:
    def __init__(self, opening_seq: SequenceSGR = None, closing_seq: SequenceSGR = None, hard_reset_after: bool = False):
        self._opening_seq: SequenceSGR = self._opt_arg(opening_seq)
        self._closing_seq: SequenceSGR = self._opt_arg(closing_seq)
        if hard_reset_after:
            self._closing_seq = SequenceSGR(sgr.RESET)

    def wrap(self, text: Any = None) -> str:
        result = self._opening_seq.print()
        if text is not None:
            result += str(text)
        result += self._closing_seq.print()
        return result

    @property
    def opening_str(self) -> str:
        return self._opening_seq.print()

    @property
    def opening_seq(self) -> SequenceSGR:
        return self._opening_seq

    @property
    def closing_str(self) -> str:
        return self._closing_seq.print()

    @property
    def closing_seq(self) -> SequenceSGR:
        return self._closing_seq

    def _opt_arg(self, arg: SequenceSGR | None) -> SequenceSGR:
        if not arg:
            return seq.NOOP
        return arg

    def __call__(self, text: Any = None) -> str:
        return self.wrap(text)

    def __eq__(self, other: Format) -> bool:
        if not isinstance(other, Format):
            return False
        return self._opening_seq == other._opening_seq and self._closing_seq == other._closing_seq

    def __repr__(self):
        return super().__repr__() + '[{!r}, {!r}]'.format(self._opening_seq, self._closing_seq)


def autof(*args: str | int | SequenceSGR) -> Format:
    opening_seq = build(*args)
    closing_seq = sgr_parity_registry.get_closing_seq(opening_seq)
    return Format(opening_seq, closing_seq)


noop = autof()
"""Special instance in cases where you *have to* select one or 
another Format, but do not want anything to be actually printed. 

- ``noop(string)`` or ``noop.wrap(string)`` returns ``string`` without any modifications;
- ``noop.opening_str`` and ``noop.closing_str`` are empty strings;
- ``noop.opening_seq`` and ``noop.closing_seq`` both returns ``seq.NOOP``.
"""

bold = autof(sgr.BOLD)
dim = autof(sgr.DIM)
italic = autof(sgr.ITALIC)
underlined = autof(sgr.UNDERLINED)
inversed = autof(sgr.INVERSED)
overlined = autof(sgr.OVERLINED)

red = autof(sgr.RED)
green = autof(sgr.GREEN)
yellow = autof(sgr.YELLOW)
blue = autof(sgr.BLUE)
magenta = autof(sgr.MAGENTA)
cyan = autof(sgr.CYAN)
gray = autof(sgr.GRAY)

bg_black = autof(sgr.BG_BLACK)
bg_red = autof(sgr.BG_RED)
bg_green = autof(sgr.BG_GREEN)
bg_yellow = autof(sgr.BG_YELLOW)
bg_blue = autof(sgr.BG_BLUE)
bg_magenta = autof(sgr.BG_MAGENTA)
bg_cyan = autof(sgr.BG_CYAN)
bg_gray = autof(sgr.BG_GRAY)
