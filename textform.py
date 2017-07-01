#!/usr/bin/python2.7

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

"""Format values with a template string like Perl format (perlform(1)).

In the template:

 @<<<<   Left justified field.
 @>>>>   Right justified field.
 @||||   Centered field.

Any other text in the template is copied through to the result.

The "~~" feature of Perl format is implied: repeat until all fields
are exhausted.

Example:

 textform.format("@<<<<<<<<:@|||||||:@>>>>>>>",
                 ["now is the time for all",
                  "good men to",
                  "come to the aid of their party"])

returns:

 "now is   : good men :  come to\n" +
 "the time :    to    :the aid of\n" +
 "for all  :          :     their\n" +
 "         :          :     party"

"""
import re
import textwrap

field_re = re.compile(r'(@[<|>]+)')
spaces_re = re.compile(r'\s+')

class Mismatch(Exception):
    pass

def format(template, values):
    """Same as format_to_lines but returns a single string."""
    return "\n".join(format_to_lines(template, values))

def format_to_lines(template, values):
    """Format 'values' into 'template'.

Returns a list of one or more lines of text.
Each line is not terminated with newline.
"""
    # Parse the template.
    fields = []
    t = template
    while True:
        m = field_re.search(t)
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
        raise Mismatch("Wrong number of values {} for number of fields {}"
                       .format(len(values), len(fields) / 2))

    # Wrap each value to the width of the corresponding field.
    values = list(values)
    for vi in xrange(len(values)):
        fi = 2 * vi + 1
        f = fields[fi]
        v = values[vi]

        v = spaces_re.sub(str(v), " ").strip()
        if f:
            v = textwrap.wrap(v, width=len(f))
        else:
            v = []

        t = f[1:2]
        if t == ">":
            justify = _justify_right
        elif t == "|":
            justify = _justify_center
        else:
            justify = _justify_left
        v = map(lambda x: justify(x, len(f)), v)

        values[vi] = v

    line = []
    more = False
    for fi in xrange(len(fields)):
        if fi % 2 == 0:
            line.append(fields[fi])
            continue
        vi = fi / 2
        v = values[vi]
        if v:
            line.append(v.pop(0))
            if v:
                more = True
        else:
            line.append(" " * len(fields[fi]))
    lines = ["".join(line).rstrip()]

    while more:
        line = []
        more = False
        for fi in xrange(len(fields)):
            if fi % 2 == 0:
                line.append(fields[fi])
                continue
            vi = fi / 2
            if not values[vi]:
                line.append(" " * len(fields[fi]))
                continue
            line.append(values[vi].pop(0))
            if values[vi]:
                more = True
        lines.append("".join(line).rstrip())

    return lines

def _justify_left(s, width):
    return s + " " * (width - len(s))

def _justify_right(s, width):
    return " " * (width - len(s)) + s

def _justify_center(s, width):
    spaces = width - len(s)
    left = spaces / 2
    return " " * left + s + " " * (spaces - left)
