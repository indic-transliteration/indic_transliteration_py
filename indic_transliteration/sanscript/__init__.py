# -*- coding: utf-8 -*-
"""
Transliteration functions for Sanskrit. The most important function is
:func:`transliterate`, which is very easy to use::

    output = transliterate(data, IAST, DEVANAGARI)

By default, the module supports the following scripts:

- Bengali
- Devanagari
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
import sys
from indic_transliteration.sanscript.schemes import Scheme
from indic_transliteration.sanscript.schemes import roman
from indic_transliteration.sanscript.schemes import brahmi

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# These variables are replicated here for backward compatibility.
# -------------
BENGALI = brahmi.BENGALI
DEVANAGARI = brahmi.DEVANAGARI
GUJARATI = brahmi.GUJARATI
GURMUKHI = brahmi.GURMUKHI
KANNADA = brahmi.KANNADA
MALAYALAM = brahmi.MALAYALAM
ORIYA = brahmi.ORIYA
TAMIL = brahmi.TAMIL
TELUGU = brahmi.TELUGU
HK = roman.HK
IAST = roman.IAST
ITRANS = roman.ITRANS
OPTITRANS = roman.OPTITRANS
KOLKATA = roman.KOLKATA
SLP1 = roman.SLP1
VELTHUIS = roman.VELTHUIS
WX = roman.WX

SCHEMES = {}


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

def _roman(data, scheme_map, **kw):
  """Transliterate `data` with the given `scheme_map`. This function is used
  when the source scheme is a Roman scheme.

  :param data: the data to transliterate
  :param scheme_map: a dict that maps between characters in the old scheme
                     and characters in the new scheme
  """
  vowels = scheme_map.vowels
  marks = scheme_map.marks
  virama = scheme_map.virama
  consonants = scheme_map.consonants
  non_marks_viraama = scheme_map.non_marks_viraama
  max_key_length_from_scheme = scheme_map.max_key_length_from_scheme
  to_roman = scheme_map.to_scheme.is_roman

  togglers = kw.pop('togglers', set())
  suspend_on = kw.pop('suspend_on', set())
  suspend_off = kw.pop('suspend_off', set())
  if kw:
    raise TypeError('Unexpected keyword argument %s' % list(kw.keys())[0])

  buf = []
  i = 0
  had_consonant = found = False
  len_data = len(data)
  append = buf.append

  # If true, don't transliterate. The toggle token is discarded.
  toggled = False
  # If true, don't transliterate. The suspend token is retained.
  # `suspended` overrides `toggled`.
  suspended = False

  while i <= len_data:
    # The longest token in the source scheme has length `max_key_length_from_scheme`. Iterate
    # over `data` while taking `max_key_length_from_scheme` characters at a time. If we don`t
    # find the character group in our scheme map, lop off a character and
    # try again.
    #
    # If we've finished reading through `data`, then `token` will be empty
    # and the loop below will be skipped.
    token = data[i:i + max_key_length_from_scheme]

    while token:
      if token in togglers:
        toggled = not toggled
        i += 2  # skip over the token
        found = True  # force the token to fill up again
        break

      if token in suspend_on:
        suspended = True
      elif token in suspend_off:
        suspended = False

      if toggled or suspended:
        token = token[:-1]
        continue

      # Catch the pattern CV, where C is a consonant and V is a vowel.
      # V should be rendered as a vowel mark, a.k.a. a "dependent"
      # vowel. But due to the nature of Brahmic scripts, 'a' is implicit
      # and has no vowel mark. If we see 'a', add nothing.
      if had_consonant and token in vowels:
        mark = marks.get(token, '')
        if mark:
          append(mark)
        elif to_roman:
          append(vowels[token])
        found = True

      # Catch any non_marks_viraama character, including consonants, punctuation,
      # and regular vowels. Due to the implicit 'a', we must explicitly
      # end any lingering consonants before we can handle the current
      # token.
      elif token in non_marks_viraama:
        if had_consonant:
          append(virama[''])
        append(non_marks_viraama[token])
        found = True

      if found:
        had_consonant = token in consonants
        i += len(token)
        break
      else:
        token = token[:-1]

    # We've exhausted the token; this must be some other character. Due to
    # the implicit 'a', we must explicitly end any lingering consonants
    # before we can handle the current token.
    if not found:
      if had_consonant:
        append(virama[''])
      if i < len_data:
        append(data[i])
        had_consonant = False
      i += 1

    found = False

  return ''.join(buf)


def _brahmic(data, scheme_map, **kw):
  """Transliterate `data` with the given `scheme_map`. This function is used
  when the source scheme is a Brahmic scheme.

  :param data: the data to transliterate
  :param scheme_map: a dict that maps between characters in the old scheme
                     and characters in the new scheme
  """
  marks = scheme_map.marks
  virama = scheme_map.virama
  consonants = scheme_map.consonants
  non_marks_viraama = scheme_map.non_marks_viraama
  to_roman = scheme_map.to_scheme.is_roman
  max_key_length_from_scheme = scheme_map.max_key_length_from_scheme

  buf = []
  i = 0
  to_roman_had_consonant = found = False
  append = buf.append
  # logging.debug(pprint.pformat(scheme_map.consonants))

  # We dont just translate each brAhmic character one after another in order to prefer concise transliterations when possible - for example ज्ञ -> jn in optitrans rather than j~n.
  while i <= len(data):
    # The longest token in the source scheme has length `max_key_length_from_scheme`. Iterate
    # over `data` while taking `max_key_length_from_scheme` characters at a time. If we don`t
    # find the character group in our scheme map, lop off a character and
    # try again.
    #
    # If we've finished reading through `data`, then `token` will be empty
    # and the loop below will be skipped.
    token = data[i:i + max_key_length_from_scheme]

    while token:
      if len(token) == 1:
        if token in marks:
          append(marks[token])
          found = True
        elif token in virama:
          append(virama[token])
          found = True
        else:
          if to_roman_had_consonant:
            append('a')
          append(non_marks_viraama.get(token, token))
          found = True
      else:
        if token in non_marks_viraama:
          if to_roman_had_consonant:
            append('a')
          append(non_marks_viraama.get(token))
          found = True

      if found:
        to_roman_had_consonant = to_roman and token in consonants
        i += len(token)
        break        
      else:
        token = token[:-1]

    # Continuing the outer while loop.
    # We've exhausted the token; this must be some other character. Due to
    # the implicit 'a', we must explicitly end any lingering consonants
    # before we can handle the current token.
    if not found:
      if to_roman_had_consonant:
        append(next(iter(virama.values())))
      if i < len(data):
        append(data[i])
        to_roman_had_consonant = False
      i += 1

    found = False

  if to_roman_had_consonant:
    append('a')
  return ''.join(buf)


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

  func = _roman if scheme_map.from_scheme.is_roman else _brahmic
  return func(data, scheme_map, **options)


def get_standard_form(data, scheme_name):
  return transliterate(data=transliterate(data=data, _from=scheme_name, _to=DEVANAGARI), _from=DEVANAGARI, _to=scheme_name)

def _setup():
  """Add a variety of default schemes."""
  s = str.split
  if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences
    s = unicode.split

  ## NOTE: See the Scheme constructor documentation for a few general notes while defining schemes.
  SCHEMES.update({
    HK: roman.HkScheme(),
    VELTHUIS: roman.VelthiusScheme(),
    OPTITRANS: roman.OptitransScheme(),
    ITRANS: roman.ItransScheme(),
    IAST: roman.IastScheme(),
    KOLKATA: roman.IastScheme(kolkata_variant=True),
    SLP1: roman.Slp1Scheme(),
    WX: roman.WxScheme(),
    BENGALI: brahmi.BengaliScheme(),
    DEVANAGARI: brahmi.DevanagariScheme(),
    GUJARATI: brahmi.GujaratiScheme(),
    GURMUKHI: brahmi.GurmukhiScheme(),
    KANNADA: brahmi.KannadaScheme(),
    MALAYALAM: brahmi.MalayalamScheme(),
    ORIYA: brahmi.OriyaScheme(),
    TAMIL: brahmi.TamilScheme(),
    TELUGU: brahmi.TeluguScheme()
  })

_setup()
