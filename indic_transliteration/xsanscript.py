# -*- coding: utf-8 -*-
"""
This is a variant of :py:mod:`~indic_transliteration.sanscript` which supports more intuitive transliteration for non-sanskrit characters in Indian languages (like hrasva e and o in draviDian ones).
"""
import copy

from indic_transliteration import sanscript

import sys

SCHEMES = {}

# Brahmi schemes
# -------------
DEVANAGARI = 'devanagari'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TAMIL = 'tamil'
TELUGU = 'telugu'

# Roman schemes
# -------------
HK = 'hk'
IAST = 'iast'
ITRANS = 'itrans'
OPTITRANS = 'optitrans'
KOLKATA = 'kolkata'
SLP1 = 'slp1'
VELTHUIS = 'velthuis'
WX = 'wx'


def transliterate(data, _from=None, _to=None, scheme_map=None, **kw):
    """Transliterate `data` with the given parameters::

      output = transliterate('idam adbhutam', HK, DEVANAGARI)

  Each time the function is called, a new :class:`SchemeMap` is created
  to map the input scheme to the output scheme. This operation is fast
  enough for most use cases. But for higher performance, you can pass a
  pre-computed :class:`SchemeMap` instead::

      scheme_map = SchemeMap(SCHEMES[HK], SCHEMES[DEVANAGARI])
      output = transliterate('idam adbhutam', scheme_map=scheme_map)

  :param data: the data to transliterate
  :param _from: the name of a source scheme
  :param _to: the name of a destination scheme
  :param scheme_map: the :class:`SchemeMap` to use. If specified, ignore
                     `_from` and `_to`. If unspecified, create a
                     :class:`SchemeMap` from `_from` to `_to`.
  """
    if scheme_map is None:
        from_scheme = SCHEMES[_from]
        to_scheme = SCHEMES[_to]
        scheme_map = sanscript.SchemeMap(from_scheme, to_scheme)

    options = {
        'togglers': {'##'},
        'suspend_on': set('<'),
        'suspend_off': set('>')
    }
    options.update(kw)

    func = sanscript._roman if scheme_map.from_roman else sanscript._brahmic
    return func(data, scheme_map, **options)


def _setup():
    """Add a variety of default schemes."""
    s = str.split
    if sys.version_info < (3, 0):
        # noinspection PyUnresolvedReferences
        s = unicode.split

    def pop_all(some_dict, some_list):
        for scheme in some_list:
            some_dict.pop(scheme)
    global SCHEMES
    SCHEMES = copy.deepcopy(sanscript.SCHEMES)
    pop_all(SCHEMES, [sanscript.ORIYA, sanscript.BENGALI, sanscript.GUJARATI])
    SCHEMES[DEVANAGARI].update({
        'vowels': SCHEMES[DEVANAGARI]['vowels'] + s("""ऎ ऒ"""),
        'marks': SCHEMES[DEVANAGARI]['marks'] + s("""ॆ ॊ"""),
        'consonants': SCHEMES[DEVANAGARI]['consonants'] + s("""ऩ ऱ ऴ""")
    })
    SCHEMES[HK].update({
        'vowels': SCHEMES[HK]['vowels'] + s("""e o"""),
        'marks': SCHEMES[HK]['marks'] + s("""e o"""),
        'consonants': SCHEMES[HK]['consonants'] + s("""n2 r2 zh""")
    })
    SCHEMES[ITRANS].update({
        'vowels': SCHEMES[ITRANS]['vowels'] + s("""e o"""),
        'marks': SCHEMES[ITRANS]['marks'] + s("""e o"""),
        'consonants': SCHEMES[ITRANS]['consonants'] + s("""n2 r2 zh""")
    })
    pop_all(SCHEMES[ITRANS].synonym_map, s("""e o"""))
    SCHEMES[OPTITRANS].update({
        'vowels': SCHEMES[OPTITRANS]['vowels'] + s("""e o"""),
        'marks': SCHEMES[OPTITRANS]['marks'] + s("""e o"""),
        'consonants': SCHEMES[OPTITRANS]['consonants'] + s("""n2 r2 zh""")
    })
    pop_all(SCHEMES[OPTITRANS].synonym_map, s("""e o"""))
    SCHEMES[IAST].update({
        'vowels': SCHEMES[ITRANS]['vowels'] + s("""ê ô"""),
        'marks': SCHEMES[ITRANS]['marks'] + s("""ê ô"""),
        'consonants': SCHEMES[ITRANS]['consonants'] + s("""n r̂ ḷ""")
    })
    SCHEMES[KANNADA].update({
        'vowels': SCHEMES[KANNADA]['vowels'] + s("""ಎ ಒ"""),
        'marks': SCHEMES[KANNADA]['marks'] + s("""ೆ ೊ"""),
        'consonants': SCHEMES[KANNADA]['consonants'] + s("""ऩ ಱ ೞ""")
    })
    SCHEMES[MALAYALAM].update({
        'vowels': SCHEMES[MALAYALAM]['vowels'] + s("""എ ഓ"""),
        'marks': SCHEMES[MALAYALAM]['marks'] + s("""െ ൊ"""),
        'consonants': SCHEMES[MALAYALAM]['consonants'] + s("""ഩ ള ൟ"""),
    })
    SCHEMES[TAMIL].update({
        'vowels': SCHEMES[TAMIL]['vowels'] + SCHEMES[TAMIL]['vowels'] + s("""எ ஒ"""),
        'marks': SCHEMES[TAMIL]['marks'] + ['ெ', 'ொ'],
        'consonants': SCHEMES[TAMIL]['consonants'] + s("""ன ற ழ""")
    })
    SCHEMES[TELUGU].update({
        'vowels': SCHEMES[TELUGU]['vowels'] + s("""ఎ ఒ"""),
        'marks': SCHEMES[TELUGU]['marks'] + s("""ె  ొ"""),
        'consonants': SCHEMES[TELUGU]['consonants'] + s("""ऩ ఴ ౚ""")
    })


_setup()
