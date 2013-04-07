# -*- coding: utf8 -*-
# SDAPS - Scripts for data acquisition with paper based surveys
# Copyright(C) 2008, 2013, Benjamin Berg <benjamin@sipsolutions.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sdaps import log
import re

try:
    from sdaps.utils.latexmap import mapping
except ImportError:
    mapping = {}
    log.warning(_(u'The latex character map is missing! Please build it using the supplied tool (create-latexmap.py).'))


re_latex_to_unicode_mapping = {}
for token, replacement in mapping.iteritems():
    regexp = re.compile(u'%s(?=^w|})' % re.escape(token))
    re_latex_to_unicode_mapping[regexp] = replacement

# Regular expressions don't work really, but we replace a single string anyways
unicode_to_latex_mapping = {}
for token, replacement in mapping.iteritems():
    unicode_to_latex_mapping[replacement] = u"{%s}" % token


def latex_to_unicode(string):
    string = unicode(string)
    for regexp, replacement in re_latex_to_unicode_mapping.iteritems():
        string, count = regexp.subn(replacement, string)

    def ret_char(match):
        return match.group('char')
    string, count = re.subn(r'\\IeC {(?P<char>.*?)}', ret_char, string)
    return string

def unicode_to_latex(string):
    string = unicode(string)
    for char, replacement in unicode_to_latex_mapping.iteritems():
        string = string.replace(char, replacement)

    # Ensure only ASCII characters are left
    return string.encode('ascii')

