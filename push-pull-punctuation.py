import scribus

STYLE_BEFORE = "Aphroconfuso: pull quote"
STYLE_AFTER  = "Aphroconfuso: pull punctuation"

QUOTES = ["”", "’"]
PUNCT  = [".", ","]

def process_frame(frame):
    text = scribus.getAllText(frame)
    length = len(text)

    for i in range(length - 1):
        first  = text[i]
        second = text[i + 1]

        # punctuation followed by quote  (.”)
        if first in PUNCT and second in QUOTES:
            scribus.selectText(i + 1, 1, frame)  # always second
            scribus.setCharacterStyle(STYLE_BEFORE, frame)

        # quote followed by punctuation (”.)
        elif first in QUOTES and second in PUNCT:
            scribus.selectText(i + 1, 1, frame)  # always second
            scribus.setCharacterStyle(STYLE_AFTER, frame)


def main():
    if not scribus.haveDoc():
        scribus.messageBox("Error", "No document open.")
        return

    items = scribus.getPageItems()

    for item in items:
        name = item[0]
        if scribus.getObjectType(name) == "TextFrame":
            process_frame(name)

    scribus.deselectAll()
    scribus.messageBox("Done", "Finished applying styles.")


if __name__ == "__main__":
    main()
