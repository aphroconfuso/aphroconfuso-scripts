replacementsx = (
    # tab and non breaking space to single space
    (r'[' + '\u0009' + '\u00a0' + r']+', '\u0020'),

    # space+hyphen+space to space+en dash+space
    ('\u0020' + '\u002d' + r'+' + '\u0020', '\u0020' + '\u2013' + '\u0020'),

    # double space to single space
    ('\u0020' + '\u0020' + r'+', '\u0020'),

    # space+solidus or solidus+space to solidus
    ('\u0020' + r'\/|\/' + '\u0020', '\u002f'),

    # space+hyphen or hyphen+space to hyphen
    ('\u0020' + r'\-|\-' + '\u0020', '\u002d'),

    # ampersand to space+ampersand; if there is not a space before the ampersand
    (r'(?<!' + '\u0020' + r')' + '\u0026', '\u0020' + '\u0026'),

    # ampersand to ampersand+space; if there is not a space after the ampersand
    ('\u0026' + r'(?!' + '\u0020' + r')', '\u0026' + '\u0020'),

    # percent sign to space+percent sign; if there is not a space before the percent sign
    # WARNING: In Slovak the percent sign is spaced if the number is used as a noun, while no space is inserted if the number is used as an adjective (e.g. “a 50% increase”).
    # Therefore consider carefully the use of the replacement.
    # (r'(?<!' + '\u0020' + r')\%', '\u0020' + '\u0025'),

    # percent sign to percent sign+space; if there are not a space, full stop, comma, semicolon, colon, question mark, exclamation mark, slovak right single quotation mark,
    # slovak right double quotation mark, new line (SHIFT+ENTER) or carriage return after the percent sign
    (r'\%(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u0025' + '\u0020'),

    # left parenthesis to space+left parenthesis; if there is not a space before the left parenthesis
    (r'(?<!' + '\u0020' + r')\(', '\u0020' + '\u0028'),

    # right parenthesis to right parenthesis+space; if there are not a space, full stop, comma, semicolon, colon, question mark, exclamation mark,
    # slovak right single quotation mark, slovak right double quotation mark, new line (SHIFT+ENTER) or carriage return after the right parenthesis
    (r'\)(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u0029' + '\u0020'),

    # left parenthesis+space to left parenthesis
    (r'\(' + '\u0020', '\u0028'),

    # space+right parenthesis to right parenthesis
    ('\u0020' + r'\)', '\u0029'),

    # three full stops to ellipsis
    (r'\.\.\.+', '\u2026'),

    # space+ellipsis to ellipsis
    ('\u0020' + '\u2026', '\u2026'),

    # double ellipsis to ellipsis
    ('\u2026' + '\u2026' + r'+', '\u2026'),

    # ellipsis to ellipsis+space; if there are not a space, question mark, exclamation mark, slovak right single quotation mark,
    # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the ellipsis
    ('\u2026' + r'(?!' + '\u0020' + r'|\?|\!|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u2026' + '\u0020'),

    # space+full stop to full stop
    ('\u0020' + r'\.', '\u002e'),

    # double full stop to full stop
    (r'\.\.+', '\u002e'),

    # full stop to full stop+space; if there are not a space, comma, semicolon, colon, slovak right single quotation mark,
    # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the full stop
    (r'\.(?!' + '\u0020' + r'|\,|\;|\:|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u002e' + '\u0020'),

    # space+comma to comma
    ('\u0020' + r'\,', '\u002c'),

    # double comma to comma
    (r'\,\,+', '\u002c'),

    # comma to comma+space; if there are not a space, number, slovak right single quotation mark, slovak right double quotation mark,
    # new line (SHIFT+ENTER) or carriage return after the comma
    (r'\,(?!' + '\u0020' + r'|[0-9]|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u002c' + '\u0020'),

    # space+colon to colon
    ('\u0020' + r'\:', '\u003a'),

    # double colon to colon
    (r'\:\:+', '\u003a'),

    # colon to colon+space; if there are not a space, new line (SHIFT+ENTER) or carriage return after the colon
    (r'\:(?!' + '\u0020' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u003a' + '\u0020'),

    # space+semicolon to semicolon
    ('\u0020' + r'\;', '\u003b'),

    # double semicolon to semicolon
    (r'\;\;+', '\u003b'),

    # semicolon to semicolon+space; if there are not a space, new line (SHIFT+ENTER) or carriage return after the semicolon
    (r'\;(?!' + '\u0020' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u003b' + '\u0020'),

    # space+question mark to question mark
    ('\u0020' + r'\?', '\u003f'),

    # question mark to question mark+space; if there are not a space, question mark, exclamation mark, slovak right single quotation mark,
    # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the question mark
    (r'\?' + r'(?!' + '\u0020' + r'|\?|\!|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u2026' + '\u0020'),

    # space+exclamation mark to exclamation mark
    ('\u0020' + r'\!', '\u0021'),

    # exclamation mark to exclamation mark+space; if there are not a space, question mark, exclamation mark, slovak right single quotation mark,
    # slovak right double quotation mark, new line (SHIFT+ENTER), carriage return or end of text after the exclamation mark
    (r'\!' + r'(?!' + '\u0020' + r'|\?|\!|' + '\u2018' + r'|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u2026' + '\u0020'),

    # slovak left single quotation mark+space to slovak left single quotation mark
    ('\u201a' + '\u0020', '\u201a'),

    # slovak left double quotation mark+space to slovak left double quotation mark
    ('\u201e' + '\u0020', '\u201e'),

    # space+slovak right single quotation mark to slovak right single quotation mark
    ('\u0020' + '\u2018', '\u2018'),

    # space+slovak right double quotation mark to slovak right double quotation mark
    ('\u0020' + '\u201c', '\u201c'),

    # slovak left single quotation mark to slovak left single quotation mark+space; if there is not a space before the slovak left single quotation mark
    (r'(?<!' + '\u0020' + r')\(', '\u0020' + '\u201a'),

    # slovak left double quotation mark to slovak left double quotation mark+space; if there is not a space before the slovak left double quotation mark
    (r'(?<!' + '\u0020' + r')\(', '\u0020' + '\u201e'),

    # slovak right single quotation mark to slovak right single quotation mark+space; if there are not a space, full stop, comma, semicolon, colon, question mark,
    # exclamation mark, slovak right double quotation mark, new line (SHIFT+ENTER) or carriage return after the slovak right single quotation mark
    ('\u2018' + r'(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!|' + '\u201c' + r'|' + '\u001c' + r'|' + '\u000d' + r')', '\u2018' + '\u0020'),

    # slovak right double quotation mark to slovak right double quotation mark+space; if there are not a space, full stop, comma, semicolon, colon, question mark,
    # exclamation mark, new line (SHIFT+ENTER), carriage return or end of text after the slovak right double quotation mark
    ('\u201c' + r'(?!' + '\u0020' + r'|\.|\,|\;|\:|\?|\!|' + '\u001c' + r'|' + '\u000d' + r'|' + r'' + r')', '\u201c' + '\u0020'),

    # new line (SHIFT+ENTER) to carriage return
    ('\u001c' + r'+', '\u000d'),

    # space+carriage return to carriage return
    ('\u0020' + '\u000d' + r'+', '\u000d'),

    # carriage return+space to carriage return
    ('\u000d' + '\u0020' + r'+', '\u000d'),

    # double carriage return to carriage return
    ('\u000d' + '\u000d' + r'+', '\u000d'),

    # remove extra spaces from start and end of a text
    (r'^' + '\u0020' + r'|' + '\u0020' + r'$', '')
)
