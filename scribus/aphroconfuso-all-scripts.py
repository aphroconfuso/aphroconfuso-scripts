import scribus
import os

SCRIPT_DIR = os.path.dirname(__file__)

def reset_text():
    if not scribus.haveDoc():
        scribus.messageBox("Error", "No document open.")
        return

    for obj in scribus.getPageItems():
        name = obj[0]
        itemtype = obj[1]

        # 4 = Text Frame
        if itemtype == 4:
            scribus.selectObject(name)

            length = scribus.getTextLength(name)
            if length == 0:
                continue

            scribus.selectText(0, length, name)
            scribus.setStyle("Aphroconfuso: Default body text", name)
            scribus.setFontSize(10.30, name)

def run_script(filename):
    path = os.path.join(SCRIPT_DIR, filename)
    exec(open(path, encoding="utf-8").read(), globals())

def main():
    scribus.statusMessage("Resetting styles...")
    reset_text()

    scribus.statusMessage("Running replacements...")
    run_script("aphroconfuso-all-fixes.py")

    scribus.statusMessage("Running section restarts...")
    run_script("aphroconfuso-section-restarts.py")

    scribus.statusMessage("Running push-pull quotation...")
    run_script("push-pull-punctuation.py")

    scribus.statusMessage("Done.")

if __name__ == "__main__":
    main()
