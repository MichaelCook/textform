#!/usr/bin/env python3

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

import unittest
import textform

class TestStringMethods(unittest.TestCase):

    def test_basic(self) -> None:
        r = textform.format('hello world', [])
        self.assertEqual(r, 'hello world')

        r = textform.format('', [])
        self.assertEqual(r, '')

    def test_wrong_number_of_values(self) -> None:
        with self.assertRaises(textform.Mismatch):
            textform.format('foo', [1])
        with self.assertRaises(textform.Mismatch):
            textform.format('@>>>', [1, 2])
        with self.assertRaises(textform.Mismatch):
            textform.format('@>>>', [])

    def test3(self) -> None:
        r = textform.format('@<<<<<< @|||||| @>>>>>>', (101, 202, 303))
        self.assertEqual(r, '101       202       303')

        r = textform.format(': @<<<<<< : @|||||| : @>>>>>> :', (101, 202, 303))
        self.assertEqual(r, ': 101     :   202   :     303 :')

    def test_left_middle_right(self) -> None:
        r = textform.format('@<<<<<<', ['foo'])
        self.assertEqual(r, 'foo')

        r = textform.format('@>>>>>>', ['foo'])
        self.assertEqual(r, '    foo')

        r = textform.format('@||||||', ['foo'])
        self.assertEqual(r, '  foo')

    # Leading whitespace in the template is preserved.
    # Trailing whitespace is not.
    def test_left_middle_right_spaces(self) -> None:
        r = textform.format('  @<<<<<<  ', ['foo'])
        self.assertEqual(r, '  foo')

        r = textform.format('  @>>>>>>  ', ['foo'])
        self.assertEqual(r, '      foo')

        r = textform.format('  @||||||  ', ['foo'])
        self.assertEqual(r, '    foo')

    def test_multiline(self) -> None:
        t = 'now is the time for all good men to come to the aid of their party'.split()
        r = textform.format('@<<<<<<<<<:@|||||||||:@>>>>>>>>>',
                            [' '.join(t),
                             ' '.join(reversed(t)),
                             ' '.join(t[:-3]).upper()])
        print('\n{}\n{}\n{}'.format('=' * 70, r, '=' * 70))
        self.assertEqual(r,
                         'now is the:  party   :NOW IS THE\n' +
                         'time for  : their of :  TIME FOR\n' +
                         'all good  :aid the to:  ALL GOOD\n' +
                         'men to    : come to  :    MEN TO\n' +
                         'come to   : men good :   COME TO\n' +
                         'the aid of: all for  :   THE AID\n' +
                         'their     : time the :\n' +
                         'party     :  is now  :')

        r = textform.format('@<<<<<<<<<:@|||||||||:@>>>>>>>>>',
                            [' '.join(t[:-3]),
                             ' '.join(reversed(t)),
                             ' '.join(t).upper()])
        print('\n{}\n{}\n{}'.format('=' * 70, r, '=' * 70))
        self.assertEqual(r,
                         'now is the:  party   :NOW IS THE\n' +
                         'time for  : their of :  TIME FOR\n' +
                         'all good  :aid the to:  ALL GOOD\n' +
                         'men to    : come to  :    MEN TO\n' +
                         'come to   : men good :   COME TO\n' +
                         'the aid   : all for  :THE AID OF\n' +
                         '          : time the :     THEIR\n' +
                         '          :  is now  :     PARTY')

        r = textform.format('@<<<<<<<<<:@|||||||||:@>>>>>>>>>',
                            [' '.join(t),
                             ' '.join(reversed(t[:-3])),
                             ' '.join(t).upper()])
        print('\n{}\n{}\n{}'.format('=' * 70, r, '=' * 70))
        self.assertEqual(r,
                         'now is the:aid the to:NOW IS THE\n' +
                         'time for  : come to  :  TIME FOR\n' +
                         'all good  : men good :  ALL GOOD\n' +
                         'men to    : all for  :    MEN TO\n' +
                         'come to   : time the :   COME TO\n' +
                         'the aid of:  is now  :THE AID OF\n' +
                         'their     :          :     THEIR\n' +
                         'party     :          :     PARTY')

        r = textform.format('@<<<<<<<<<<:@>>>>>>>>>>',
                            ['now-is-the-time-for-all-good-men',
                             'hello-world'])
        print('\n{}\n{}\n{}'.format('=' * 70, r, '=' * 70))
        self.assertEqual(r,
                         'now-is-the-:hello-world\n' +
                         'time-for-  :\n' +
                         'all-good-  :\n' +
                         'men        :')

        r = textform.format('@<<<<<<<<:@|||||||||:@>>>>>>>>>',
                            ['now is the time for all',
                             'good men to',
                             'come to the aid of their party'])
        print('\n{}\n{}\n{}'.format('=' * 70, r, '=' * 70))
        self.assertEqual(r,
                         'now is   : good men :   come to\n' +
                         'the time :    to    :the aid of\n' +
                         'for all  :          :     their\n' +
                         '         :          :     party')

if __name__ == '__main__':
    unittest.main()
