# -*- coding: utf-8 -*-
"""
Transliteration functions for Sanskrit. The most important function is
:func:`transliterate`, which is very easy to use::

    output = transliterate(data, IAST, DEVANAGARI)

By default, the module supports the following scripts:

- Bengali
- Devanagari
- Gunjala Gondi
- Gujarati
- Kannada
- Malayalam
- Telugu
- Tamil
- Oriya
- Gurmukhi/ Punjabi/ Panjabi

and the following romanizations:

- HK = 'hk'
- IAST = 'iast'
- ITRANS = 'itrans'
- OPTITRANS = 'optitrans'
- KOLKATA_v2 = 'kolkata_v2'
- SLP1 = 'slp1'
- VELTHUIS = 'velthuis'
- WX = 'wx'

Each of these **schemes** is defined in a global dictionary `SCHEMES`, whose
keys are strings::

    devanagari_scheme = SCHEMES['devanagari']

For convenience, we also define a variable for each scheme::

    devanagari_scheme = SCHEMES[DEVANAGARI]

These variables are documented below.

:license: MIT and BSD

.. _Bengali: http://en.wikipedia.org/wiki/Bengali_alphabet
.. _Devanagari: http://en.wikipedia.org/wiki/Devanagari
.. _Gujarati: http://en.wikipedia.org/wiki/Gujarati_alphabet
.. _Kannada: http://en.wikipedia.org/wiki/Kannada_alphabet
.. _Malayalam: http://en.wikipedia.org/wiki/Malayalam_alphabet
.. _Telugu: http://en.wikipedia.org/wiki/Telugu_alphabet

.. _Harvard-Kyoto: http://en.wikipedia.org/wiki/Harvard-Kyoto
.. _IAST: http://en.wikipedia.org/wiki/IAST
"""

from __future__ import unicode_literals

# Brahmic schemes
# ---------------
#: Internal name of Bengali. Bengali ``ba`` and ``va`` are both rendered
#: as `ব`.
from indic_transliteration.sanscript.schemes import Scheme
from indic_transliteration.sanscript.schemes import roman
from indic_transliteration.sanscript.schemes import brahmic

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# These variables are replicated here for backward compatibility.
# -------------
BENGALI = brahmic.BENGALI
DEVANAGARI = brahmic.DEVANAGARI
GUNJALA_GONDI = brahmic.GUNJALA_GONDI
GUJARATI = brahmic.GUJARATI
GURMUKHI = brahmic.GURMUKHI
KANNADA = brahmic.KANNADA
MALAYALAM = brahmic.MALAYALAM
ORIYA = brahmic.ORIYA
TAMIL = brahmic.TAMIL
GRANTHA = brahmic.GRANTHA
TELUGU = brahmic.TELUGU
TITUS = roman.TITUS
HK = roman.HK
IAST = roman.IAST
ISO = roman.ISO
ITRANS = roman.ITRANS
OPTITRANS = roman.OPTITRANS
KOLKATA = roman.KOLKATA_v2
KOLKATA_v2 = roman.KOLKATA_v2
SLP1 = roman.SLP1
VELTHUIS = roman.VELTHUIS
WX = roman.WX

## NOTE: See the Scheme constructor documentation for a few general notes while defining schemes.
SCHEMES = {}
SCHEMES.update(roman.SCHEMES)
SCHEMES.update(brahmic.SCHEMES)

class SchemeMap(object):
  """Maps one :class:`Scheme` to another. This class grabs the metadata and
  character data required for :func:`transliterate`.

  :param from_scheme: the source scheme
  :param to_scheme: the destination scheme
  """

  def __init__(self, from_scheme, to_scheme):
    """Create a mapping from `from_scheme` to `to_scheme`."""
    self.vowel_marks = {}
    self.virama = {}

    self.vowels = {}
    self.consonants = {}
    self.non_marks_viraama = {}
    self.accents = {}
    self.from_scheme = from_scheme
    self.to_scheme = to_scheme
    self.max_key_length_from_scheme = max(len(x) for g in from_scheme
                                          for x in from_scheme[g])

    for group in from_scheme.keys():
      if group in ["alternates", "accented_vowel_alternates"]:
        continue
      if group not in to_scheme.keys():
        continue
      conjunct_map = {}
      for key, value in from_scheme[group].items():
        if from_scheme.name in roman.CAPITALIZABLE_SCHEME_IDS:
          if key in ["ॐ"]:
            continue
        if key in to_scheme[group]:
          from_scheme_symbol = from_scheme[group][key]
          to_scheme_symbol = to_scheme[group][key]
          if (to_scheme_symbol == "") and (group not in ["virama", "zwj", "skip"]):
            to_scheme_symbol = from_scheme_symbol
          conjunct_map[from_scheme_symbol] = to_scheme_symbol
          if from_scheme_symbol in from_scheme.get("alternates", {}):
            for k_syn in from_scheme["alternates"][from_scheme_symbol]:
              conjunct_map[k_syn] = to_scheme_symbol
      if group.endswith('vowel_marks'):
        self.vowel_marks.update(conjunct_map)
      elif group == 'virama':
        self.virama = conjunct_map
      else:
        self.non_marks_viraama.update(conjunct_map)
        if group.endswith('consonants'):
          self.consonants.update(conjunct_map)
        elif group.endswith('vowels'):
          self.vowels.update(conjunct_map)
        elif group == 'accents':
          self.accents = conjunct_map

    for base_accented_vowel, synonyms in from_scheme.get("accented_vowel_alternates", {}).items():
      for accented_vowel in synonyms:
        base_vowel = base_accented_vowel[:-1]
        source_accent = base_accented_vowel[-1]
        # Roman a does not map to any brAhmic vowel mark. Hence "" below.
        target_accent = self.accents.get(source_accent, source_accent)
        self.vowel_marks[accented_vowel] = self.vowel_marks.get(base_vowel, "") + target_accent
        self.vowels[accented_vowel] = self.vowels[base_vowel] + target_accent
        self.non_marks_viraama.update(self.vowels)


  def __str__(self):
    import pprint
    return pprint.pformat({"vowels": self.vowels,
                           "vowel_marks":  self.vowel_marks,
                           "virama":  self.virama,
                           "consonants": self.consonants})


@lru_cache(maxsize=8)
def _get_scheme_map(input_encoding, output_encoding):
    """Provides a caching layer on top of `SchemeMap` objects to allow faster
    access to scheme maps we've instantiated once.

    :param input_encoding: Input encoding. Must be defined in `SCHEMES`.
    :param output_encoding: Input encoding. Must be defined in `SCHEMES`.
    """
    return SchemeMap(SCHEMES[input_encoding], SCHEMES[output_encoding])


def transliterate(data, _from=None, _to=None, scheme_map=None, **kw):
  """Transliterate `data` with the given parameters::

      output = transliterate('idam adbhutam', HK, DEVANAGARI)

  Common options: togglers= {'##'}, suspend_on= set('<'), suspend_off = set('>')

  Each time the function is called, a new :class:`SchemeMap` is created
  to map the input scheme to the output scheme. This operation is fast
  enough for most use cases. But for higher performance, you can pass a
  pre-computed :class:`SchemeMap` instead::

      scheme_map = SchemeMap(SCHEMES[HK], SCHEMES[DEVANAGARI])
      output = transliterate('idam adbhutam', scheme_map=scheme_map)

  :param data: the data to transliterate
  :param scheme_map: the :class:`SchemeMap` to use. If specified, ignore
                     `_from` and `_to`. If unspecified, create a
                     :class:`SchemeMap` from `_from` to `_to`.
  """
  options = {
    'togglers': {},
    'suspend_on': set(),
    'suspend_off': set()
  }
  options.update(kw)

  if scheme_map is None:
    if _from is None:
      from indic_transliteration import detect
      _from = detect.detect(data)
    maybe_use_dravidian_variant = options.get('maybe_use_dravidian_variant', None)
    if maybe_use_dravidian_variant == "yes":
      if _from in ["kannada", "tamil", "telugu", "malayalam"]:
        dravidian_scheme = _to + "_dravidian"
        if dravidian_scheme in SCHEMES.keys():
          _to = dravidian_scheme
      elif _from in ["optitrans", "itrans", "hk"]:
        _from = _from + "_dravidian"
    elif maybe_use_dravidian_variant == "force":
      dravidian_scheme = _to + "_dravidian"
      if dravidian_scheme in SCHEMES.keys():
        _to = dravidian_scheme
    scheme_map = _get_scheme_map(_from, _to)

  from indic_transliteration.sanscript.brahmic_mapper import _brahmic
  from indic_transliteration.sanscript.roman_mapper import _roman
  func = _roman if scheme_map.from_scheme.is_roman else _brahmic
  data = scheme_map.from_scheme.unapply_shortcuts(data_in=data)
  result = func(data, scheme_map, **options)
  result = scheme_map.to_scheme.apply_shortcuts(data_in=result)
  return result


def get_standard_form(data, scheme_name):
  return transliterate(data=transliterate(data=data, _from=scheme_name, _to=DEVANAGARI), _from=DEVANAGARI, _to=scheme_name)
