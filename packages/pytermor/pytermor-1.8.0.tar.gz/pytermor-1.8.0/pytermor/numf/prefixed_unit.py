# -----------------------------------------------------------------------------
# pytermor [ANSI formatted terminal output toolset]
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from math import trunc
from typing import List

from . import format_auto_float


@dataclass
class PrefixedUnitPreset:
    max_value_len: int
    integer_input: bool
    unit: str|None
    unit_separator: str|None
    mcoef: float
    prefixes: List[str|None]|None
    prefix_zero_idx: int|None

    @property
    def max_len(self) -> int:
        result = self.max_value_len
        result += len(self.unit_separator or '')
        result += len(self.unit or '')
        result += max([len(p) for p in self.prefixes if p])
        return result


PREFIXES_SI = ['y', 'z', 'a', 'f', 'p', 'n', 'μ', 'm', None, 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
PREFIX_ZERO_SI = 8

PRESET_SI_METRIC = PrefixedUnitPreset(
    max_value_len=4,
    integer_input=False,
    unit='m',
    unit_separator=' ',
    mcoef=1000.0,
    prefixes=PREFIXES_SI,
    prefix_zero_idx=PREFIX_ZERO_SI,
)
"""
Suitable for formatting any SI unit with values
from approximately `10^-27` to `10^27`.

``max_value_len`` must be at least **4**, because it's a
minimum requirement for displaying values from `999` to `-999`.
Next number to `999` is `1000`, which will be displayed as ``1k``.

Total maximum length is ``max_value_len + 3 =`` **7** (+3 is from separator,
unit and prefix, assuming all of them have 1-char width).
"""

PRESET_SI_BINARY = PrefixedUnitPreset(
    max_value_len=5,
    integer_input=True,
    unit='b',
    unit_separator=' ',
    mcoef=1024.0,
    prefixes=PREFIXES_SI,
    prefix_zero_idx=PREFIX_ZERO_SI,
)
"""
Similar to ``PRESET_SI_METRIC``, but this preset differs in
 one aspect.  Given a variable with default value = `995`, printing
it's value out using this preset results in ``995 b``. After
increasing it by `20` we'll have `1015`, but it's still not enough
to become a kilobyte -- so displayed value will be ``1015 b``. Only
after one more increasing (at *1024* and more) the value will be
in a form of ``1.00 kb``.  

So, in this case``max_value_len`` must be at least **5** (not 4),
because it's a minimum requirement for displaying values from `1023` 
to `-1023`.

Total maximum length is ``max_value_len + 3 =`` **8** (+3 is from separator,
unit and prefix, assuming all of them have 1-char width).
"""


def format_prefixed_unit(value: float, preset: PrefixedUnitPreset = None) -> str:
    """
    Format *value* using *preset* settings. The main idea of this method
    is to fit into specified string length as much significant digits as it's
    theoretically possible, using multipliers and unit prefixes to
    indicate them.

    Default *preset* is PRESET_SI_BINARY, PrefixedUnitPreset with base 1024
    made for binary sizes (bytes, kbytes, Mbytes).

    :param value: input value
    :param preset: formatter settings
    :return: formatted value
    :rtype: str
    """
    if preset is None:
        preset = PRESET_SI_BINARY

    prefixes = preset.prefixes or ['']
    unit_separator = preset.unit_separator or ''
    unit_idx = preset.prefix_zero_idx or ''

    while 0 <= unit_idx < len(prefixes):
        if 0.0 < abs(value) <= 1/preset.mcoef:
            value *= preset.mcoef
            unit_idx -= 1
            continue
        elif abs(value) >= preset.mcoef:
            value /= preset.mcoef
            unit_idx += 1
            continue

        unit_full = (prefixes[unit_idx] or '') + (preset.unit or '')

        if preset.integer_input and unit_idx == preset.prefix_zero_idx:
            num_str = f'{trunc(value)!s:.{preset.max_value_len}s}'
        else:
            num_str = format_auto_float(value, preset.max_value_len)

        return f'{num_str.strip()}{unit_separator}{unit_full}'

    # no more prefixes left
    return f'{value!r:{preset.max_value_len}.{preset.max_value_len}}{preset.unit_separator or ""}' + \
           '?' * max([len(p) for p in prefixes if p]) + \
           (preset.unit or "")
