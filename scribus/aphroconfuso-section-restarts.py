#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scribus
import re
import sys

SECTION_STYLE = "Aphroconfuso: Section restart"

HASH_RE = re.compile(r'^\s*#\s*$')
EMPTY_RE = re.compile(r'^\s*$')


def normalize(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def main():

    if not scribus.haveDoc():
        scribus.messageBox("Error", "No document open.")
        return

    if scribus.selectionCount() != 1:
        scribus.messageBox(
            "Error",
            "Please select exactly one text frame."
        )
        return

    frame = scribus.getSelectedObject()

    if scribus.getObjectType(frame) != "TextFrame":
        scribus.messageBox(
            "Error",
            "Selected object is not a text frame."
        )
        return

    while True:

        text = normalize(scribus.getAllText(frame))
        paragraphs = text.split("\n")

        pos = 0
        found = False

        for i, para in enumerate(paragraphs):

            if not HASH_RE.match(para):
                pos += len(para) + 1
                continue

            # Beginning of deletion
            start_para = i
            while start_para > 0 and EMPTY_RE.match(paragraphs[start_para - 1]):
                start_para -= 1

            # End of deletion
            end_para = i
            while end_para + 1 < len(paragraphs) and EMPTY_RE.match(paragraphs[end_para + 1]):
                end_para += 1

            # Character positions
            start = sum(len(p) + 1 for p in paragraphs[:start_para])
            end = sum(len(p) + 1 for p in paragraphs[:end_para + 1])

            # Delete the marker and surrounding blank paragraphs
            scribus.selectText(start, end - start, frame)
            scribus.deleteText(frame)

            # Apply Section Restart to the next paragraph
            new_text = normalize(scribus.getAllText(frame))

            if start < len(new_text):
                para_end = new_text.find("\n", start)
                if para_end == -1:
                    para_end = len(new_text)

                scribus.selectText(start, para_end - start, frame)
                scribus.setParagraphStyle(SECTION_STYLE, frame)

            found = True
            break

        if not found:
            break

    scribus.deselectAll()
    scribus.messageBox("Done", "Section restarts processed.")


if __name__ == "__main__":
    main()
