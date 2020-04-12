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
- KOLKATA = 'kolkata'
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
from indic_transliteration.sanscript.schemes.brahmic import northern, central, southern, eastern

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# These variables are replicated here for backward compatibility.
# -------------
BENGALI = eastern.BENGALI
DEVANAGARI = northern.DEVANAGARI
GUNJALA_GONDI = central.GUNJALA_GONDI
GUJARATI = northern.GUJARATI
GURMUKHI = northern.GURMUKHI
KANNADA = southern.KANNADA
MALAYALAM = southern.MALAYALAM
ORIYA = eastern.ORIYA
TAMIL = southern.TAMIL
GRANTHA = southern.GRANTHA
TELUGU = southern.TELUGU
TITUS = roman.TITUS
HK = roman.HK
IAST = roman.IAST
ITRANS = roman.ITRANS
OPTITRANS = roman.OPTITRANS
KOLKATA = roman.KOLKATA
SLP1 = roman.SLP1
VELTHUIS = roman.VELTHUIS
WX = roman.WX

## NOTE: See the Scheme constructor documentation for a few general notes while defining schemes.
SCHEMES = {}
SCHEMES.update(roman.SCHEMES)

BRAHMIC_SCHEMES = {}
BRAHMIC_SCHEMES.update(northern.SCHEMES)
BRAHMIC_SCHEMES.update(central.SCHEMES)
BRAHMIC_SCHEMES.update(southern.SCHEMES)
BRAHMIC_SCHEMES.update(eastern.SCHEMES)

SCHEMES.update(BRAHMIC_SCHEMES)

class SchemeMap(object):
  """Maps one :class:`Scheme` to another. This class grabs the metadata and
  character data required for :func:`transliterate`.

  :param from_scheme: the source scheme
  :param to_scheme: the destination scheme
  """

  def __init__(self, from_scheme, to_scheme):
    """Create a mapping from `from_scheme` to `to_scheme`."""
    self.marks = {}
    self.virama = {}

    self.vowels = {}
    self.consonants = {}
    self.non_marks_viraama = {}
    self.from_scheme = from_scheme
    self.to_scheme = to_scheme
    self.max_key_length_from_scheme = max(len(x) for g in from_scheme
                                          for x in from_scheme[g])

    for group in from_scheme.keys():
      if group not in to_scheme.keys():
        continue
      conjunct_map = {}
      for (k, v) in zip(from_scheme[group], to_scheme[group]):
        conjunct_map[k] = v
        if k in from_scheme.synonym_map:
          for k_syn in from_scheme.synonym_map[k]:
            conjunct_map[k_syn] = v
      if group.endswith('marks'):
        self.marks.update(conjunct_map)
      elif group == 'virama':
        self.virama = conjunct_map
      else:
        self.non_marks_viraama.update(conjunct_map)
        if group.endswith('consonants'):
          self.consonants.update(conjunct_map)
        elif group.endswith('vowels'):
          self.vowels.update(conjunct_map)

    if from_scheme.name == OPTITRANS:
      if len(to_scheme['virama']) == 0:
        to_scheme_virama = ""
      else:
        to_scheme_virama = to_scheme['virama'][0]
      conjunct_map = {
        "nk": self.consonants["~N"] + to_scheme_virama + self.consonants["k"],
        "nkh": self.consonants["~N"] + to_scheme_virama + self.consonants["kh"],
        "nx": self.consonants["~N"] + to_scheme_virama + self.consonants["x"],
        "ng": self.consonants["~N"] + to_scheme_virama +self.consonants["g"],
        "ngh": self.consonants["~N"] + to_scheme_virama +self.consonants["gh"],
        "nch": self.consonants["~n"] + to_scheme_virama +self.consonants["ch"],
        "nCh": self.consonants["~n"] + to_scheme_virama +self.consonants["Ch"],
        "nj": self.consonants["~n"] + to_scheme_virama +self.consonants["j"],
        "njh": self.consonants["~n"] + to_scheme_virama +self.consonants["jh"],
      }
      self.consonants.update(conjunct_map)
      self.non_marks_viraama.update(conjunct_map)
      synonym_conjunct_map = {}
      for key in conjunct_map.keys():
        latter_consonant = key[1:]
        if latter_consonant in from_scheme.synonym_map:
          for k_syn in from_scheme.synonym_map[latter_consonant]:
            synonym_conjunct_map["n" + k_syn] = conjunct_map[key]
      self.consonants.update(synonym_conjunct_map)
      self.non_marks_viraama.update(synonym_conjunct_map)

    if to_scheme.name == OPTITRANS:
      inv_map = {v: k for k, v in self.consonants.items()}
      if len(from_scheme['virama']) == 0:
          from_scheme_virama = ''
      else:
          from_scheme_virama = from_scheme['virama'][0]
      conjunct_map = {
        inv_map["~N"] + from_scheme_virama + inv_map["k"]: "nk",
        inv_map["~N"] + from_scheme_virama + inv_map["kh"]: "nkh",
        inv_map["~N"] + from_scheme_virama + inv_map["g"]: "ng",
        inv_map["~N"] + from_scheme_virama + inv_map["gh"]: "ngh",
        inv_map["~n"] + from_scheme_virama + inv_map["ch"]: "nch",
        inv_map["~n"] + from_scheme_virama + inv_map["Ch"]: "nCh",
        inv_map["~n"] + from_scheme_virama + inv_map["j"]: "nj",
        inv_map["~n"] + from_scheme_virama + inv_map["jh"]: "njh",
      }
      self.consonants.update(conjunct_map)
      self.non_marks_viraama.update(conjunct_map)

  def __str__(self):
    import pprint
    return pprint.pformat({"vowels": self.vowels,
                           "marks":  self.marks,
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
  if scheme_map is None:
    scheme_map = _get_scheme_map(_from, _to)
  options = {
    'togglers': {'##'},
    'suspend_on': set('<'),
    'suspend_off': set('>')
  }
  options.update(kw)

  from indic_transliteration.sanscript.brahmic_mapper import _brahmic
  from indic_transliteration.sanscript.roman_mapper import _roman
  func = _roman if scheme_map.from_scheme.is_roman else _brahmic
  return func(data, scheme_map, **options)


def get_standard_form(data, scheme_name):
  return transliterate(data=transliterate(data=data, _from=scheme_name, _to=DEVANAGARI), _from=DEVANAGARI, _to=scheme_name)
