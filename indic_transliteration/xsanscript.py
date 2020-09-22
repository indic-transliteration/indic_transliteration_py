# -*- coding: utf-8 -*-
"""
This is a variant of :py:mod:`~indic_transliteration.sanscript` which supports more intuitive transliteration for non-sanskrit characters in Indian languages (like hrasva e and o in draviDian ones).
"""
import copy

from indic_transliteration import sanscript

SCHEMES = {}

# Brahmi schemes
# -------------
DEVANAGARI = 'devanagari'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TAMIL = 'tamil'
GRANTHA = 'grantha'
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
    return sanscript.transliterate(data=data, scheme_map=scheme_map)


def _setup():
    """Add a variety of default schemes."""

    def pop_all(some_dict, some_list):
        for scheme in some_list:
            some_dict.pop(scheme)
    global SCHEMES
    SCHEMES = copy.deepcopy(sanscript.SCHEMES)
    pop_all(SCHEMES, [sanscript.ORIYA, sanscript.BENGALI, sanscript.GUJARATI])
    SCHEMES[HK].update({
        'vowels': str.split("""a A i I u U R RR lR lRR E ai O au""") + str.split("""e o"""),
        'marks': str.split("""A i I u U R RR lR lRR E ai O au""") + str.split("""e o"""),
        'consonants': sanscript.SCHEMES[HK]['consonants'] + str.split("""n2 r2 zh""")
    })
    SCHEMES[ITRANS].update({
        'vowels': str.split("""a A i I u U R RR LLi LLI E ai O au""") + str.split("""e o"""),
        'marks': str.split("""A i I u U R RR LLi LLI E ai O au""") + str.split("""e o"""),
        'consonants': sanscript.SCHEMES[ITRANS]['consonants'] + str.split("""n2 r2 zh""")
    })
    pop_all(SCHEMES[ITRANS].synonym_map, str.split("""e o"""))
    SCHEMES[OPTITRANS].update({
        'vowels': str.split("""a A i I u U R RR LLi LLI E ai O au""") + str.split("""e o"""),
        'marks': str.split("""A i I u U R RR LLi LLI E ai O au""") + str.split("""e o"""),
        'consonants': sanscript.SCHEMES[OPTITRANS]['consonants'] + str.split("""n2 r2 zh""")
    })
    pop_all(SCHEMES[OPTITRANS].synonym_map, str.split("""e o"""))


_setup()
