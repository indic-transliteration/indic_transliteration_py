# -*- coding: utf-8 -*-
"""
Transliteration functions for Sanskrit. The most important function is
:func:`transliterate`, which is very easy to use::

    output = transliterate(data, IAST, DEVANAGARI)

By default, the module supports the following scripts:

- Bengali_
- Devanagari_
- Gujarati_
- Kannada_
- Malayalam_
- Telugu_
- Tamil_
- Oriya_
- Gurmukhi/ Punjabi/ Panjabi_

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

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# Brahmi schemes
# -------------
BENGALI = 'bengali'
DEVANAGARI = 'devanagari'
GUJARATI = 'gujarati'
GURMUKHI = 'gurmukhi'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
ORIYA = 'oriya'
TAMIL = 'tamil'
TELUGU = 'telugu'

# Roman schemes
# -------------
HK = 'hk'
IAST = 'iast'
ITRANS = 'itrans'

"""Optitransv1 is described in https://sanskrit-coders.github.io/site/pages/input/optitrans.html#optitrans-v1 . OPTITRANS, while staying close to ITRANS it provides a more intuitive transliteration compared to ITRANS (shankara manju - शङ्कर मञ्जु)."""
OPTITRANS = 'optitrans'
KOLKATA = 'kolkata'
SLP1 = 'slp1'
VELTHUIS = 'velthuis'
WX = 'wx'

SCHEMES = {}


class Scheme(dict):
  """Represents all of the data associated with a given scheme. In addition
  to storing whether or not a scheme is roman, :class:`Scheme` partitions
  a scheme's characters into important functional groups.

  :class:`Scheme` is just a subclass of :class:`dict`.

  :param data: a :class:`dict` of initial values. Note that the particular characters present here are also assumed to be the _preferred_ transliterations when transliterating to this scheme. 
  :param synonym_map: A map from keys appearing in `data` to lists of symbols with equal meaning. For example: M -> ['.n', .'m'] in ITRANS. This synonym_map is not used in transliterating to this scheme.
  :param is_roman: `True` if the scheme is a romanization and `False`
                   otherwise.
  """

  def __init__(self, data=None, synonym_map=None, is_roman=True, name=None):
    super(Scheme, self).__init__(data or {})
    if synonym_map is None:
      synonym_map = {}
    self.synonym_map = synonym_map
    self.is_roman = is_roman
    self.name = name


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


def _setup():
  """Add a variety of default schemes."""
  s = str.split
  if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences
    s = unicode.split

  ## NOTE: See the Scheme constructor documentation for a few general notes while defining schemes.
  SCHEMES.update({
    BENGALI: Scheme({
      'vowels': s("""অ আ ই ঈ উ ঊ ঋ ৠ ঌ ৡ এ ঐ ও ঔ"""),
      'marks': s("""া ি ী ু ূ ৃ ৄ ৢ ৣ ে ৈ ো ৌ"""),
      'virama': s('্'),
      'yogavaahas': s('ং ঃ ঁ'),
      'consonants': s("""
                            ক খ গ ঘ ঙ
                            চ ছ জ ঝ ঞ
                            ট ঠ ড ঢ ণ
                            ত থ দ ধ ন
                            প ফ ব ভ ম
                            য র ল ব
                            শ ষ স হ
                            ळ ক্ষ জ্ঞ
                            """),
      'symbols': s("""
                       ॐ ঽ । ॥
                       ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯
                       """)
    }, is_roman=False, name=BENGALI),
    DEVANAGARI: Scheme({
      'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ"""),
      'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ"""),
      'virama': s('्'),
      'yogavaahas': s('ं ः ँ'),
      'consonants': s("""
                            क ख ग घ ङ
                            च छ ज झ ञ
                            ट ठ ड ढ ण
                            त थ द ध न
                            प फ ब भ म
                            य र ल व
                            श ष स ह
                            ळ क्ष ज्ञ
                            """),
      'symbols': s("""
                       ॐ ऽ । ॥
                       ० १ २ ३ ४ ५ ६ ७ ८ ९
                       """)
    }, is_roman=False, name=DEVANAGARI),
    GUJARATI: Scheme({
      'vowels': s("""અ આ ઇ ઈ ઉ ઊ ઋ ૠ ઌ ૡ એ ઐ ઓ ઔ"""),
      'marks': s("""ા િ ી ુ ૂ ૃ ૄ ૢ ૣ ે ૈ ો ૌ"""),
      'virama': s('્'),
      'yogavaahas': s('ં ઃ ઁ'),
      'consonants': s("""
                            ક ખ ગ ઘ ઙ
                            ચ છ જ ઝ ઞ
                            ટ ઠ ડ ઢ ણ
                            ત થ દ ધ ન
                            પ ફ બ ભ મ
                            ય ર લ વ
                            શ ષ સ હ
                            ળ ક્ષ જ્ઞ
                            """),
      'symbols': s("""
                       ૐ ઽ ૤ ૥
                       ૦ ૧ ૨ ૩ ૪ ૫ ૬ ૭ ૮ ૯
                       """)
    }, is_roman=False, name=GUJARATI),
    GURMUKHI: Scheme({
      'vowels': s("""ਅ ਆ ਇ ਈ ਉ ਊ ऋ ॠ ऌ ॡ ਏ ਐ ਓ ਔ"""),
      'marks': ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', '', '',
                '', '', 'ੇ', 'ੈ', 'ੋ', 'ੌ'],
      'virama': s('੍'),
      'yogavaahas': s('ਂ ਃ ਁ'),
      'consonants': s("""
                            ਕ ਖ ਗ ਘ ਙ
                            ਚ ਛ ਜ ਝ ਞ
                            ਟ ਠ ਡ ਢ ਣ
                            ਤ ਥ ਦ ਧ ਨ
                            ਪ ਫ ਬ ਭ ਮ
                            ਯ ਰ ਲ ਵ
                            ਸ਼ ਸ਼ ਸ ਹ
                            ਲ਼ ਕ੍ਸ਼ ਜ੍ਞ
                            """),
      'symbols': s("""
                       ੴ ఽ । ॥
                       ੦ ੧ ੨ ੩ ੪ ੫ ੬ ੭ ੮ ੯
                       """)
    }, is_roman=False, name=GURMUKHI),
    HK: Scheme({
      'vowels': s("""a A i I u U R RR lR lRR e ai o au"""),
      'marks': s("""A i I u U R RR lR lRR e ai o au"""),
      'virama': [''],
      'yogavaahas': s('M H ~'),
      'consonants': s("""
                            k kh g gh G
                            c ch j jh J
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            z S s h
                            L kS jJ
                            """),
      'symbols': s("""
                       OM ' | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, name=HK, synonym_map={"|": ["."], "||": [".."]}),
    VELTHUIS: Scheme({
      'vowels': s("""a aa i ii u uu .r .rr .l .ll e ai o au"""),
      'marks': s("""aa i ii u uu .r .rr .l .ll e ai o au"""),
      'virama': [''],
      'yogavaahas': s('.m .h /'),
      'consonants': s("""
                            k kh g gh "n
                            c ch j jh ~n
                            .t .th .d .dh .n
                            t th d dh n
                            p ph b bh m
                            y r l v
                            "s .s s h
                            L k.s j~n
                            """),
      'symbols': s("""
                       O .a | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, name=VELTHUIS),
    OPTITRANS: Scheme({
      'vowels': s("""a A i I u U R RR LLi LLI e ai o au"""),
      'marks': s("""A i I u U R RR LLi LLI e ai o au"""),
      'virama': [''],
      'yogavaahas': s('M H .N'),
      'consonants': s("""
                            k kh g gh ~N
                            ch Ch j jh ~n
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            sh Sh s h
                            L x jn
                            """),
      # All those special conversions like nk -> ङ्क् are hard-coded when this scheme definition is consumed to produce a scheme map. Hence, they don't show up here.
      'symbols': s("""
                       OM .a | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, synonym_map={
      "A": ["aa"], "I": ["ii"], "U": ["uu"], "e": ["E"], "o": ["O"], "R": ["R^i", "RRi"], "RR": ["R^I", "RRI"], "LLi": ["L^i"], "LLI": ["L^I"],
      "M": [".m", ".n"],
      "kh": ["K"], "gh": ["G"],
      "ch": ["c"], "Ch": ["C"], "jh": ["J"],
      "ph": ["P"], "bh": ["B"], "Sh": ["S"],
      "v": ["w"], "x": ["kSh", "kS", "ksh"], "jn": ["GY", "jJN"],
      "|": ["."], "||": [".."]
    }, name=OPTITRANS),
    ITRANS: Scheme({
      'vowels': s("""a A i I u U RRi RRI LLi LLI e ai o au"""),
      'marks': s("""A i I u U RRi RRI LLi LLI e ai o au"""),
      'virama': [''],
      'yogavaahas': s('M H .N'),
      'consonants': s("""
                            k kh g gh ~N
                            ch Ch j jh ~n
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            sh Sh s h
                            L kSh j~n
                            """),
      'symbols': s("""
                       OM .a | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, synonym_map={
      "A": ["aa"], "I": ["ii"], "U": ["uu"], "e": ["E"], "o": ["O"], "RRi": ["R^i"], "RRI": ["R^I"], "LLi": ["L^i"], "LLI": ["L^I"],
      "M": [".m", ".n"], "v": ["w"], "kSh": ["x", "kS"], "j~n": ["GY", "jJN"],
      "||": [".."], "|": ["."],
    }, name=ITRANS),
    IAST: Scheme({
      'vowels': s("""a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"""),
      'marks': s("""ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"""),
      'virama': [''],
      'yogavaahas': s('ṃ ḥ m̐'),
      'consonants': s("""
                            k kh g gh ṅ
                            c ch j jh ñ
                            ṭ ṭh ḍ ḍh ṇ
                            t th d dh n
                            p ph b bh m
                            y r l v
                            ś ṣ s h
                            ḻ kṣ jñ
                            """),
      'symbols': s("""
                       oṃ ' । ॥
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, name=IAST),
    KOLKATA: Scheme({
      'vowels': s("""a ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au"""),
      'marks': s("""ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au"""),
      'virama': [''],
      'yogavaahas': s('ṃ ḥ m̐'),
      'consonants': s("""
                            k kh g gh ṅ
                            c ch j jh ñ
                            ṭ ṭh ḍ ḍh ṇ
                            t th d dh n
                            p ph b bh m
                            y r l v
                            ś ṣ s h
                            ḻ kṣ jñ
                            """),
      'symbols': s("""
                       oṃ ' । ॥
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, name=IAST),
    KANNADA: Scheme({
      'vowels': s("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ"""),
      'marks': s("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೇ ೈ ೋ ೌ"""),
      'virama': s('್'),
      'yogavaahas': s('ಂ ಃ ँ'),
      'consonants': s("""
                            ಕ ಖ ಗ ಘ ಙ
                            ಚ ಛ ಜ ಝ ಞ
                            ಟ ಠ ಡ ಢ ಣ
                            ತ ಥ ದ ಧ ನ
                            ಪ ಫ ಬ ಭ ಮ
                            ಯ ರ ಲ ವ
                            ಶ ಷ ಸ ಹ
                            ಳ ಕ್ಷ ಜ್ಞ
                            """),
      'symbols': s("""
                       ಓಂ ऽ । ॥
                       ೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯
                       """)
    }, is_roman=False, name=KANNADA),
    MALAYALAM: Scheme({
      'vowels': s("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ"""),
      'marks': s("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ േ ൈ ോ ൌ"""),
      'virama': s('്'),
      'yogavaahas': s('ം ഃ ँ'),
      'consonants': s("""
                            ക ഖ ഗ ഘ ങ
                            ച ഛ ജ ഝ ഞ
                            ട ഠ ഡ ഢ ണ
                            ത ഥ ദ ധ ന
                            പ ഫ ബ ഭ മ
                            യ ര ല വ
                            ശ ഷ സ ഹ
                            ള ക്ഷ ജ്ഞ
                            """),
      'symbols': s("""
                       ഓം ഽ । ॥
                       ൦ ൧ ൨ ൩ ൪ ൫ ൬ ൭ ൮ ൯
                       """)
    }, is_roman=False, name=MALAYALAM),
    ORIYA: Scheme({
      'vowels': s("""ଅ ଆ ଇ ଈ ଉ ଊ ଋ ୠ ଌ ୡ ଏ ଐ ଓ ଔ"""),
      'marks': ['ା', 'ି', 'ୀ', 'ୁ', 'ୂ', 'ୃ', 'ୄ',
                '', '', 'େ', 'ୈ', 'ୋ', 'ୌ'],
      'virama': s('୍'),
      'yogavaahas': s('ଂ ଃ ଁ'),
      'consonants': s("""
                            କ ଖ ଗ ଘ ଙ
                            ଚ ଛ ଜ ଝ ଞ
                            ଟ ଠ ଡ ଢ ଣ
                            ତ ଥ ଦ ଧ ନ
                            ପ ଫ ବ ଭ ମ
                            ଯ ର ଲ ଵ
                            ଶ ଷ ସ ହ
                            ଳ କ୍ଷ ଜ୍ଞ
                            """),
      'symbols': s("""
                       ଓଂ ଽ । ॥
                       ୦ ୧ ୨ ୩ ୪ ୫ ୬ ୭ ୮ ୯
                       """)
    }, is_roman=False, name=ORIYA),
    SLP1: Scheme({
      'vowels': s("""a A i I u U f F x X e E o O"""),
      'marks': s("""A i I u U f F x X e E o O"""),
      'virama': [''],
      'yogavaahas': s('M H ~'),
      'consonants': s("""
                            k K g G N
                            c C j J Y
                            w W q Q R
                            t T d D n
                            p P b B m
                            y r l v
                            S z s h
                            L kz jY
                            """),
      'symbols': s("""
                       oM ' . ..
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, name=SLP1),
    WX: Scheme({
      'vowels': s("""a A i I u U q Q L ḹ e E o O"""),
      'marks': s("""A i I u U q Q L ḹ e E o O"""),
      'virama': [''],
      'yogavaahas': s('M H ~'),
      'consonants': s("""
                            k K g G f
                            c C j J F
                            t T d D N
                            w W x X n
                            p P b B m
                            y r l v
                            S R s h
                            ḻ kR jF
                            """),
      'symbols': s("""
                       oM ' . ..
                       0 1 2 3 4 5 6 7 8 9
                       """)
    }, name=WX),
    TAMIL: Scheme({
      'vowels': s("""அ ஆ இ ஈ உ ஊ ऋ ॠ ऌ ॡ ஏ ஐ ஓ ஔ"""),
      'marks': ['ா', 'ி', 'ீ', 'ு', 'ூ', '', '',
                '', '', 'ே', 'ை', 'ோ', 'ௌ'],
      'virama': s('்'),
      'yogavaahas': s('ஂ ஃ ँ'),
      'consonants': s("""
                            க க க க ங
                            ச ச ஜ ச ஞ
                            ட ட ட ட ண
                            த த த த ந
                            ப ப ப ப ம
                            ய ர ல வ
                            ஶ ஷ ஸ ஹ
                            ள க்ஷ ஜ்ஞ
                            """),
      'symbols': s("""
                       ௐ ऽ । ॥
                       ௦ ௧ ௨ ௩ ௪ ௫ ௬ ௭ ௮ ௯
                       """)
    }, is_roman=False, name=TAMIL),
    TELUGU: Scheme({
      'vowels': s("""అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ"""),
      'marks': s("""ా ి ీ ు ూ ృ ౄ ౢ ౣ ే ై ో ౌ"""),
      'virama': s('్'),
      'yogavaahas': s('ం ః ఁ'),
      'consonants': s("""
                            క ఖ గ ఘ ఙ
                            చ ఛ జ ఝ ఞ
                            ట ఠ డ ఢ ణ
                            త థ ద ధ న
                            ప ఫ బ భ మ
                            య ర ల వ
                            శ ష స హ
                            ళ క్ష జ్ఞ
                            """),
      'symbols': s("""
                       ఓం ఽ । ॥
                       ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯
                       """)
    }, is_roman=False, name=TELUGU)
  })

_setup()
