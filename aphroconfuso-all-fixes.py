#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# based on https://wiki.scribus.net/canvas/Clean-up_the_imported_text_based_on_the_Slovak_typographic_rules
"""
Author: Richard Sitányi (cdbox@zilina.net)
File: clean-up.py (Clean-up the imported text based on the Slovak typographic rules.)
Version: 1.0
Date: 06/02/2013

LICENSE:
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not,
write to the Free Software Foundation, Inc., 59 Temple Place – Suite 330, Boston, MA 02111-1307, USA.

DESCRIPTION:
A common problem when receiving text from other people is that it is often not as consistently formatted as you might like. Some common things that need to be fixed are:
* removing double spaces
* removing spaces before full stops, commas, colons, semicolons, question marks or exclamation marks
* removing extra spaces or tabs at the beginning and at the end of the paragraphs
* removing blank lines between paragraphs
Fixing these items manually can become very time consuming. This script will help you clean-up the imported text based on the Slovak typographic rules.

USAGE:
Create new document, insert text frame, import text from file, run the script and enjoy ;-)

"""

import sys
import re

try:
    import scribus
except ImportError as err:
    print('This Python script is written for the Scribus scripting interface. It can only be run from within Scribus.')
    sys.exit(1)

if not scribus.haveDoc():
    scribus.messageBox('Warning', 'You should open a document.', scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)
if scribus.selectionCount() == 0:
    scribus.messageBox('Warning', 'You should select a text frame.', scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)
if scribus.selectionCount() > 1:
    scribus.messageBox('Warning', 'You should select one text frame.', scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)

replacements = (
    # Artikli
    (r' ’l ', ' ’l\u00a0'),
    (r' ’l-', ' ’l\u2011'),

    (r' il-', ' il\u2011'),
    (r' l-', ' l\u2011'),

    (r' ir-', ' ir\u2011'),
    (r' r-', ' r\u2011'),

    (r' is-', ' is\u2011'),
    (r' s-', ' s\u2011'),

    (r' it-', ' it\u2011'),
    (r' t-', ' t\u2011'),

    (r' iċ-', ' iċ\u2011'),
    (r' ċ-', ' ċ\u2011'),

    (r' id-', ' id\u2011'),
    (r' d-', ' d\u2011'),

    (r' in-', ' in\u2011'),
    (r' n-', ' n\u2011'),

    (r' ix-', ' ix\u2011'),
    (r' x-', ' x\u2011'),

    (r' iz-', ' iz\u2011'),
    (r' z-', ' z\u2011'),

    (r' iż-', ' iż\u2011'),
    (r' ż-', ' ż\u2011'),

    # Artikli (kapitali)
    (r' Il-', ' Il\u2011'),
    (r' L-',   ' L\u2011'),
    (r' Ir-', ' Ir\u2011'),
    (r' Is-', ' Is\u2011'),
    (r' It-', ' It\u2011'),
    (r' Iċ-', ' Iċ\u2011'),
    (r' Id-', ' Id\u2011'),
    (r' In-', ' In\u2011'),
    (r' Ix-', ' Ix\u2011'),
    (r' Iz-', ' Iz\u2011'),
    (r' Iż-', ' Iż\u2011'),

    (r' bl-', ' bl\u2011'),
    (r' Bl-', ' Bl\u2011'),

    (r' fl-', ' fl\u2011'),
    (r' Fl-', ' Fl\u2011'),

    # new line (SHIFT+ENTER) to carriage return
    ('\u001c' + r'+', '\u000d'),

    # space+carriage return to carriage return
    ('\u0020' + '\u000d' + r'+', '\u000d'),

    # carriage return+space to carriage return
    ('\u000d' + '\u0020' + r'+', '\u000d'),

    # double carriage return to carriage return
    ('\u000d' + '\u000d' + r'+', '\u000d'),

    # remove extra spaces from start and end of a text
    (r'^' + '\u0020' + r'|' + '\u0020' + r'$', ''),

    # three full stops to ellipsis
    (r'\.\.\.+', '\u2026'),

    # add narrow spaces to em dash
    ('\u2014', '\u202f' + '\u200b' + '\u2014' + '\u200b' + '\u202f'),

    # clean up double narrow spaces
    ('\u2009' + '\u2009', '\u2009'),

    # double space to single space
    ('\u0020' + '\u0020' + r'+', '\u0020'),

    # tab and non breaking space to single space
    ('\u0009', '\u0020'),

    # add narrow spaces to em dash
    ('\u2044', '\u200b' + '\u2044' + '\u200b'),

		# add hair space to slash, replace normal spaces
    ('/', '\u200a' + '/' + '\u0020'),
    ('\u0020' + r'+' + '/' + '\u0020' + r'+', '\u200a' + '/' + '\u0020'),

    # Sezzjonijiet ġodda
    ('\u0023' + '\u0020', '\u0023'),
    ('\u000d' + '\u0023' + '\u000d', '\u000d' + '\u0023' + '\u0020'),
    ('\u000d' + '\u000d', '\u000d'),
    ('\u000d' + '\u0023', '\u000d' + '\u000d' + '\u0023'),


		# ADD
		#  ’l => add thin space before and nbsp after
		#  ’l- => add thin space before
    #      ’’ also add thin space
    # [ ’] add thin space before


		# make one for ragged; all nb hyphens, and no one- or two-letter words at the end of a line
)

d = scribus.getSelectedObject()

if scribus.getObjectType(d) != 'TextFrame':
    scribus.messageBox('Warning', 'You should select a text frame.', scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)
else:
    try:
        for item in replacements:
            content = scribus.getAllText(d)
            print(f'Processing replacement: {item}')
            p = re.compile(item[0])
            r = re.finditer(p, content) # , re.IGNORECASE
            for i in reversed(tuple(r)):
                count = i.end() - i.start()
                print(f'Found match at {i.start()} to {i.end()}, length {count}')
                scribus.selectText(i.start(), count, d)
                print(f'Selected text from {i.start()} for {count} characters')
                scribus.deleteText(d)
                print(f'Deleted text from {i.start()}')
                scribus.insertText(item[1], i.start(), d)
                print(f'Inserted "{item[1]}" at {i.start()}')
    except IndexError as e:
        print(f'IndexError: {e}')
        sys.exit(1)

scribus.messageBox('Lest!', 'Aphroconfuso: it-tindif lest!', scribus.ICON_WARNING, scribus.BUTTON_OK)
