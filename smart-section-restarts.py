import scribus
import re

SECTION_STYLE = "Aphroconfuso: Section restart"
CHAR_STYLE = "Aphroconfuso: Small capitals"

HASH_RE = re.compile(r'^\s*#\s*$')
EMPTY_RE = re.compile(r'^\s*$')
WORD_RE = re.compile(r'\b[\w’]+(?:-[\w’]+)*\b', re.UNICODE)

def normalize_breaks(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')

def process_frame(frame):
    text = normalize_breaks(scribus.getAllText(frame))
    paragraphs = text.split('\n')

    # Compute start indices of each paragraph
    para_positions = []
    pos = 0
    for para in paragraphs:
        para_positions.append((para, pos))
        pos += len(para) + 1  # +1 for newline

    remove_ranges = []  # list of (start_idx, end_idx) to delete
    section_restart_positions = []  # positions to style

    i = 0
    while i < len(paragraphs):
        para, start_idx = para_positions[i]
        if HASH_RE.match(para):
            # Find start of deletion
            remove_start = i
            while remove_start > 0 and EMPTY_RE.match(paragraphs[remove_start - 1]):
                remove_start -= 1

            # Find end of deletion
            remove_end = i + 1
            while remove_end < len(paragraphs) and EMPTY_RE.match(paragraphs[remove_end]):
                remove_end += 1

            # Track the paragraph after removed block for Section Restart
            if remove_end < len(paragraphs):
                _, target_idx = para_positions[remove_end]
                section_restart_positions.append(target_idx)
                scribus.statusMessage(f"Paragraph {remove_end+1} will be Section Restart styled")

            # Track deletion range
            start_pos = para_positions[remove_start][1]
            if remove_end - 1 < len(para_positions):
                _, end_pos = para_positions[remove_end - 1]
                end_pos += len(paragraphs[remove_end - 1]) + 1
            else:
                end_pos = len(text)
            remove_ranges.append((start_pos, end_pos))
            i = remove_end
        else:
            i += 1

    # Delete ranges in reverse order to keep positions valid
    for start, end in reversed(remove_ranges):
        scribus.selectText(start, end - start, frame)
        scribus.deleteText(frame)
        scribus.statusMessage(f"Deleted text from {start} to {end}")

    # Apply styles to first-three-word paragraph positions
    for start_idx in section_restart_positions:
        text_after = scribus.getAllText(frame)
        if start_idx >= len(text_after):
            continue
        # Find end of paragraph
        end_idx = text_after.find('\n', start_idx)
        if end_idx == -1:
            end_idx = len(text_after)
        para_text = text_after[start_idx:end_idx]

        # Paragraph style
        scribus.selectText(start_idx, len(para_text), frame)
        scribus.setParagraphStyle(SECTION_STYLE, frame)

        # First 3 words
        matches = list(WORD_RE.finditer(para_text))
        if len(matches) >= 3:
            end_pos = matches[2].end()
            first_part = para_text[:end_pos]
            lower_part = first_part.lower()
            scribus.selectText(start_idx, len(first_part), frame)
            scribus.deleteText(frame)
            scribus.insertText(lower_part, start_idx, frame)
            scribus.selectText(start_idx, len(first_part), frame)
            scribus.setCharacterStyle(CHAR_STYLE, frame)

def main():
    if not scribus.haveDoc():
        scribus.messageBox("Error", "No document open.")
        return

    for item in scribus.getPageItems():
        if item[1] == 4:  # text frame
            process_frame(item[0])

if __name__ == "__main__":
    main()
