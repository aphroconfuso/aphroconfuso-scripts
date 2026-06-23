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
		(r' L-', 	' L\u2011'),
		(r' Ir-', ' Ir\u2011'),
		(r' Is-', ' Is\u2011'),
		(r' It-', ' It\u2011'),
		(r' Iċ-', ' Iċ\u2011'),
		(r' Id-', ' Id\u2011'),
		(r' In-', ' In\u2011'),
		(r' Ix-', ' Ix\u2011'),
		(r' Iz-', ' Iz\u2011'),
		(r' Iż-', ' Iż\u2011'),

		# add narrow spaces to em dash
		('\u2014', '\u2009' + '\u2014' + '\u2009'),

		# clean up double narrow spaces
    ('\u2009' + '\u2009', '\u2009'),

		# clean up double new lines
    ('\u000d' + '\u000d' + r'+', '\u000d'),

		# double space to single space
		('\u0020' + '\u0020' + r'+', '\u0020'),

    # tab and non breaking space to single space
    ('\u0009', ''),

)

# replacementsx = (
# 		# Artikli
# 		(r'(^|\s)([żiI]ż)-', r'\g<1>\g<2>\u2011', re.IGNORECASE),

#     # space+hyphen+space to space+en dash+space
#     ('\u0020' + '\u002d' + r'+' + '\u0020', '\u0020' + '\u2013' + '\u0020'),

#     # space+solidus or solidus+space to solidus
#     ('\u0020' + r'\/|\/' + '\u0020', '\u002f'),

#     # space+hyphen or hyphen+space to hyphen
#     ('\u0020' + r'\-|\-' + '\u0020', '\u002d'),

#     # ampersand to space+ampersand; if there is not a space before the ampersand
#     (r'(?<!' + '\u0020' + r')' + '\u0026', '\u0020' + '\u0026'),

#     # ampersand to ampersand+space; if there is not a space after the ampersand
#     ('\u0026' + r'(?!' + '\u0020' + r')', '\u0026' + '\u0020'),

#     # percent sign to space+percent sign; if there is not a space before the percent sign
#     # WARNING: In Slovak the percent sign is spaced if the number is used as a noun, while no space is inserted if the number is used as an adjective (e.g. “a 50% increase”).
#     # Therefore consider carefully the use of the replacement.
#     # (r'(?<!' + '\u0020' + r')\%', '\u0020' + '\u0025'),

#     # percent sign to percent sign+space; if there are not a space, full stop, comma, semicolon, colon, question mark, exclamation mark, slovak right single quotation mark,
#     # slovak right double quotation mark, new line (SHIFT+ENTER) or carriage return after the percent sign
#     (r'\%(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u0025' + '\u0020'),

#     # left parenthesis to space+left parenthesis; if there is not a space before the left parenthesis
#     (r'(?<!' + '\u0020' + r')\(', '\u0020' + '\u0028'),

#     # right parenthesis to right parenthesis+space; if there are not a space, full stop, comma, semicolon, colon, question mark, exclamation mark,
#     # slovak right single quotation mark, slovak right double quotation mark, new line (SHIFT+ENTER) or carriage return after the right parenthesis
#     (r'\)(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u0029' + '\u0020'),

#     # left parenthesis+space to left parenthesis
#     (r'\(' + '\u0020', '\u0028'),

#     # space+right parenthesis to right parenthesis
#     ('\u0020' + r'\)', '\u0029'),

#     # three full stops to ellipsis
#     (r'\.\.\.+', '\u2026'),

#     # space+ellipsis to ellipsis
#     ('\u0020' + '\u2026', '\u2026'),

#     # double ellipsis to ellipsis
#     ('\u2026' + '\u2026' + r'+', '\u2026'),

#     # ellipsis to ellipsis+space; if there are not a space, question mark, exclamation mark, slovak right single quotation mark,
#     # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the ellipsis
#     ('\u2026' + r'(?!' + '\u0020' + r'|\?|\!|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u2026' + '\u0020'),

#     # space+full stop to full stop
#     ('\u0020' + r'\.', '\u002e'),

#     # double full stop to full stop
#     (r'\.\.+', '\u002e'),

#     # full stop to full stop+space; if there are not a space, comma, semicolon, colon, slovak right single quotation mark,
#     # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the full stop
#     (r'\.(?!' + '\u0020' + r'|\,|\;|\:|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u002e' + '\u0020'),

#     # space+comma to comma
#     ('\u0020' + r'\,', '\u002c'),

#     # double comma to comma
#     (r'\,\,+', '\u002c'),

#     # comma to comma+space; if there are not a space, number, slovak right single quotation mark, slovak right double quotation mark,
#     # new line (SHIFT+ENTER) or carriage return after the comma
#     (r'\,(?!' + '\u0020' + r'|[0-9]|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u002c' + '\u0020'),

#     # space+colon to colon
#     ('\u0020' + r'\:', '\u003a'),

#     # double colon to colon
#     (r'\:\:+', '\u003a'),

#     # colon to colon+space; if there are not a space, new line (SHIFT+ENTER) or carriage return after the colon
#     (r'\:(?!' + '\u0020' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u003a' + '\u0020'),

#     # space+semicolon to semicolon
#     ('\u0020' + r'\;', '\u003b'),

#     # double semicolon to semicolon
#     (r'\;\;+', '\u003b'),

#     # semicolon to semicolon+space; if there are not a space, new line (SHIFT+ENTER) or carriage return after the semicolon
#     (r'\;(?!' + '\u0020' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u003b' + '\u0020'),

#     # space+question mark to question mark
#     ('\u0020' + r'\?', '\u003f'),

#     # question mark to question mark+space; if there are not a space, question mark, exclamation mark, slovak right single quotation mark,
#     # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the question mark
#     (r'\?' + r'(?!' + '\u0020' + r'|\?|\!|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u2026' + '\u0020'),

#     # space+exclamation mark to exclamation mark
#     ('\u0020' + r'\!', '\u0021'),

#     # exclamation mark to exclamation mark+space; if there are not a space, question mark, exclamation mark, slovak right single quotation mark,
#     # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the exclamation mark
#     (r'\!' + r'(?!' + '\u0020' + r'|\?|\!|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u2026' + '\u0020'),

#     # slovak left single quotation mark+space to slovak left single quotation mark
#     ('\u201a' + '\u0020', '\u201a'),

#     # slovak left double quotation mark+space to slovak left double quotation mark
#     ('\u201e' + '\u0020', '\u201e'),

#     # space+slovak right single quotation mark to slovak right single quotation mark
#     ('\u0020' + '\u2018', '\u2018'),

#     # space+slovak right double quotation mark to slovak right double quotation mark
#     ('\u0020' + '\u201c', '\u201c'),

#     # slovak left single quotation mark to slovak left single quotation mark+space; if there is not a space before the slovak left single quotation mark
#     (r'(?<!' + '\u0020' + r')\(', '\u0020' + '\u201a'),

#     # slovak left double quotation mark to slovak left double quotation mark+space; if there is not a space before the slovak left double quotation mark
#     (r'(?<!' + '\u0020' + r')\(', '\u0020' + '\u201e'),

#     # slovak right single quotation mark to slovak right single quotation mark+space; if there are not a space, full stop, comma, semicolon, colon, question mark,
#     # exclamation mark, slovak right double quotation mark, new line (SHIFT+ENTER) or carriage return after the slovak right single quotation mark
#     ('\u2018' + r'(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u2018' + '\u0020'),

#     # slovak right double quotation mark to slovak right double quotation mark+space; if there are not a space, full stop, comma, semicolon, colon, question mark,
#     # exclamation mark, new line (SHIFT+ENTER), carriage return or end of text after the slovak right double quotation mark
#     ('\u201c' + r'(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u201c' + '\u0020'),

#     # new line (SHIFT+ENTER) to carriage return
#     ('\u001c' + r'+', '\u000d'),

#     # space+carriage return to carriage return
#     ('\u0020' + '\u000d' + r'+', '\u000d'),

#     # carriage return+space to carriage return
#     ('\u000d' + '\u0020' + r'+', '\u000d'),

#     # double carriage return to carriage return
#     ('\u000d' + '\u000d' + r'+', '\u000d'),

#     # remove extra spaces from start and end of a text
#     (r'^' + '\u0020' + r'|' + '\u0020' + r'$', '')
# )

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
