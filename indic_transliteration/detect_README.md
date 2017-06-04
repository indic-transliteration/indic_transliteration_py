detect.py
=========

When handling a Sanskrit string, it's almost always best to explicitly state
its transliteration scheme. This avoids embarrassing errors with words
like `pitRRIn`. But most of the time, it's possible to infer the encoding
from the text itself.

`detect.py` automatically detects a string's transliteration scheme:

    detect('pitRRIn') == Scheme.ITRANS
    detect('pitRRn') == Scheme.HK
    detect('pitFn') == Scheme.SLP1
    detect('पितॄन्') == Scheme.Devanagari
    detect('পিতৄন্') == Scheme.Bengali

Supported schemes
-----------------

All schemes are attributes on the `Scheme` class. You can also just use the
scheme name:

    Scheme.IAST == 'IAST'
    Scheme.Devanagari == 'Devanagari'

Scripts:

- Bengali (`'Bengali'`)
- Devanagari (`'Devanagari'`)
- Gujarati (`'Gujarati'`)
- Gurmukhi (`'Gurmukhi'`)
- Kannada (`'Kannada'`)
- Malayalam (`'Malayalam'`)
- Oriya (`'Oriya'`)
- Tamil (`'Tamil'`)
- Telugu (`'Telugu'`)

Romanizations:

- Harvard-Kyoto (`'HK'`)
- IAST (`'IAST'`)
- ITRANS (`'ITRANS'`)
- Kolkata (`'Kolkata'`)
- SLP1 (`'SLP1'`)
- Velthuis (`'Velthuis'`)
