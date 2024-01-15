# This software is distributed under the "Simplified BSD license":
#
# Copyright Michael Cook <michael@waxrat.com>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Format values with a template string like Perl format (perlform(1)).

In the template:

 @<<<<   Left justified field.
 @>>>>   Right justified field.
 @||||   Centered field.

Any other text in the template is copied through to the result.

The '~~' feature of Perl format is implied: repeat until all fields
are exhausted.

Example:

 textform.format('@<<<<<<<<:@|||||||:@>>>>>>>',
                 ['now is the time for all',
                  'good men to',
                  'come to the aid of their party'])

returns:

 'now is   : good men :  come to\n' +
 'the time :    to    :the aid of\n' +
 'for all  :          :     their\n' +
 '         :          :     party'

"""
import re
import textwrap
from typing import Any, Final
from collections.abc import Sequence

_FIELD_RE: Final = re.compile(r'(@[<|>]+)')
_SPACES_RE: Final = re.compile(r'\s+')

def _cleanup_spaces(v: str) -> str:
    return _SPACES_RE.sub(str(v), ' ').strip()

def _justify_left(s: str, width: int) -> str:
    return s + ' ' * (width - len(s))

def _justify_right(s: str, width: int) -> str:
    return ' ' * (width - len(s)) + s

def _justify_center(s: str, width: int) -> str:
    spaces = width - len(s)
    left = spaces // 2
    return ' ' * left + s + ' ' * (spaces - left)

class Mismatch(Exception):
    pass

def format(template: str, values: str | Sequence[Any]) -> str:  # pylint: disable=redefined-builtin
    """
    Same as format_to_lines but returns a single string
    """
    if not isinstance(values, list):
        values = list(values)
    return '\n'.join(format_to_lines(template, values))

def format_to_lines(template: str, values: Sequence[Any]) -> list[str]:
    """
    Format 'values' into 'template'.

    Returns a list of one or more lines of text.
    Each line is not terminated with newline.
    """

    # Parse the template.
    fields: list[str] = []
    t = template
    while True:
        m = _FIELD_RE.search(t)
        if not m:
            break
        a, z = m.span(0)
        fields.extend((t[0:a], t[a:z]))
        t = t[z:]
    fields.append(t)

    # len(fields)>=1.  The even fields are to be used literally.  The odd
    # fields are @... template fields.  [0] and [-1] always exist, they're
    # literals, they might be the empty string, and they might be the same
    # string (i.e., if len(fields)==1).

    if len(values) * 2 + 1 != len(fields):
        raise Mismatch(f'Wrong number of values {len(values)} '
                       f'for number of fields {len(fields) // 2}')

    # Wrap each value to the width of the corresponding field.
    rows = []
    for vi in range(len(values)):  # pylint: disable=consider-using-enumerate
        fi = 2 * vi + 1
        f = fields[fi]
        v = values[vi]

        vs = textwrap.wrap(_cleanup_spaces(v), width=len(f)) if f else []

        t = f[1:2]
        if t == '>':
            justify = _justify_right
        elif t == '|':
            justify = _justify_center
        else:
            justify = _justify_left

        rows.append(list(justify(x, len(f)) for x in vs))

    line = []
    more = False
    for fi, f in enumerate(fields):
        if fi % 2 == 0:
            line.append(f)
            continue
        vi = fi // 2
        row = rows[vi]
        if row:
            line.append(row.pop(0))
            if row:
                more = True
        else:
            line.append(' ' * len(f))
    lines = [''.join(line).rstrip()]

    while more:
        line = []
        more = False
        for fi, f in enumerate(fields):
            if fi % 2 == 0:
                line.append(f)
                continue
            vi = fi // 2
            if not rows[vi]:
                line.append(' ' * len(f))
                continue
            line.append(rows[vi].pop(0))
            if rows[vi]:
                more = True
        lines.append(''.join(line).rstrip())

    return lines
