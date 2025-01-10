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

sectionRestartReplacements = (
    # find and replace hash+new line+hash+new line with new line
    ('\u000d' + '\u0023' + '\u000d', '\u000d'),
)

d = scribus.getSelectedObject()

if scribus.getObjectType(d) != 'TextFrame':
    scribus.messageBox('Warning', 'You should select a text frame.', scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)
else:
    try:
        for item in sectionRestartReplacements:
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
                scribus.selectText(i.start()+10, 10, d)
                scribus.setStyle('Aphroconfuso: Section restart', d)
                scribus.deselectAll()
                print(f'Inserted "{item[1]}" at {i.start()}')
    except IndexError as e:
        print(f'IndexError: {e}')
        sys.exit(1)

scribus.messageBox('Done', 'Aphroconfuso clean-up done.', scribus.ICON_WARNING, scribus.BUTTON_OK)
