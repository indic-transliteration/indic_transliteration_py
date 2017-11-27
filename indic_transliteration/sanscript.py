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

and the following romanizations:

- Harvard-Kyoto_
- IAST_ (also known as Roman Unicode)
- SLP1
- WX

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
import logging
import sys

import regex

BENGALI = 'bengali'

#: Internal name of Devanagari.
DEVANAGARI = 'devanagari'

#: Internal name of Gujarati.
GUJARATI = 'gujarati'

#: Internal name of Gurmukhi.
GURMUKHI = 'gurmukhi'

#: Internal name of Kannada.
KANNADA = 'kannada'

#: Internal name of Malayalam.
MALAYALAM = 'malayalam'

#: Internal name of Oriya.
ORIYA = 'oriya'

#: Internal name of Tamil.
TAMIL = 'tamil'

#: Internal name of Telugu.
TELUGU = 'telugu'

# Roman schemes
# -------------
#: Internal name of Harvard-Kyoto.
HK = 'hk'

#: Internal name of IAST.
IAST = 'iast'

#: Internal name of ITRANS
ITRANS = 'itrans'

#: Internal name of KOLKATA
KOLKATA = 'kolkata'

#: Internal name of SLP1.
SLP1 = 'slp1'

#: Internal name of Velthuis.
VELTHUIS = 'velthuis'

#: Internal name of WX.
WX = 'wx'

SCHEMES = {}


class Scheme(dict):
  """Represents all of the data associated with a given scheme. In addition
  to storing whether or not a scheme is roman, :class:`Scheme` partitions
  a scheme's characters into important functional groups.

  :class:`Scheme` is just a subclass of :class:`dict`.

  :param data: a :class:`dict` of initial values.
  :param synonym_map: A map from keys appearing in `data` to lists of symbols with equal meaning. For example: M -> ['.n', .'m'] in ITRANS. 
  :param is_roman: `True` if the scheme is a romanization and `False`
                   otherwise.
  """

  def __init__(self, data=None, synonym_map=None, is_roman=True):
    super(Scheme, self).__init__(data or {})
    if synonym_map is None:
      synonym_map = {}
    self.synonym_map = synonym_map
    self.is_roman = is_roman


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
    self.other = {}
    self.from_roman = from_scheme.is_roman
    self.to_roman = to_scheme.is_roman
    self.longest = max(len(x) for g in from_scheme
                       for x in from_scheme[g])

    for group in from_scheme:
      if group not in to_scheme:
        continue
      sub_map = {}
      for (k, v) in zip(from_scheme[group], to_scheme[group]):
        sub_map[k] = v
        if k in from_scheme.synonym_map:
          for k_syn in from_scheme.synonym_map[k]:
            sub_map[k_syn] = v
      if group.endswith('marks'):
        self.marks.update(sub_map)
      elif group == 'virama':
        self.virama = sub_map
      else:
        self.other.update(sub_map)
        if group.endswith('consonants'):
          self.consonants.update(sub_map)
        elif group.endswith('vowels'):
          self.vowels.update(sub_map)


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
  other = scheme_map.other
  longest = scheme_map.longest
  to_roman = scheme_map.to_roman

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
    # The longest token in the source scheme has length `longest`. Iterate
    # over `data` while taking `longest` characters at a time. If we don`t
    # find the character group in our scheme map, lop off a character and
    # try again.
    #
    # If we've finished reading through `data`, then `token` will be empty
    # and the loop below will be skipped.
    token = data[i:i + longest]

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

      # Catch any other character, including consonants, punctuation,
      # and regular vowels. Due to the implicit 'a', we must explicitly
      # end any lingering consonants before we can handle the current
      # token.
      elif token in other:
        if had_consonant:
          append(virama[''])
        append(other[token])
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
  other = scheme_map.other
  to_roman = scheme_map.to_roman

  buf = []
  had_consonant = False
  append = buf.append

  for L in data:
    if L in marks:
      append(marks[L])
    elif L in virama:
      append(virama[L])
    else:
      if had_consonant:
        append('a')
      append(other.get(L, L))
    had_consonant = to_roman and L in consonants

  if had_consonant:
    append('a')
  return ''.join(buf)


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
    scheme_map = SchemeMap(from_scheme, to_scheme)

  options = {
    'togglers': {'##'},
    'suspend_on': set('<'),
    'suspend_off': set('>')
  }
  options.update(kw)

  func = _roman if scheme_map.from_roman else _brahmic
  return func(data, scheme_map, **options)


def _setup():
  """Add a variety of default schemes."""
  s = str.split
  if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences
    s = unicode.split

  SCHEMES.update({
    BENGALI: Scheme({
      'vowels': s("""অ আ ই ঈ উ ঊ ঋ ৠ ঌ ৡ এ ঐ ও ঔ"""),
      'marks': s("""া ি ী ু ূ ৃ ৄ ৢ ৣ ে ৈ ো ৌ"""),
      'virama': s('্'),
      'other': s('ং ঃ ঁ'),
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
    }, is_roman=False),
    DEVANAGARI: Scheme({
      'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ"""),
      'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ"""),
      'virama': s('्'),
      'other': s('ं ः ँ'),
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
    }, is_roman=False),
    GUJARATI: Scheme({
      'vowels': s("""અ આ ઇ ઈ ઉ ઊ ઋ ૠ ઌ ૡ એ ઐ ઓ ઔ"""),
      'marks': s("""ા િ ી ુ ૂ ૃ ૄ ૢ ૣ ે ૈ ો ૌ"""),
      'virama': s('્'),
      'other': s('ં ઃ ઁ'),
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
    }, is_roman=False),
    GURMUKHI: Scheme({
      'vowels': s("""ਅ ਆ ਇ ਈ ਉ ਊ ऋ ॠ ऌ ॡ ਏ ਐ ਓ ਔ"""),
      'marks': ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', '', '',
                '', '', 'ੇ', 'ੈ', 'ੋ', 'ੌ'],
      'virama': s('੍'),
      'other': s('ਂ ਃ ਁ'),
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
                       ॐ ऽ । ॥
                       ੦ ੧ ੨ ੩ ੪ ੫ ੬ ੭ ੮ ੯
                       """)
    }, is_roman=False),
    HK: Scheme({
      'vowels': s("""a A i I u U R RR lR lRR e ai o au"""),
      'marks': s("""A i I u U R RR lR lRR e ai o au"""),
      'virama': [''],
      'other': s('M H ~'),
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
    }),
    ITRANS: Scheme({
      'vowels': s("""a A i I u U RRi RRI LLi LLI e ai o au"""),
      'marks': s("""A i I u U RRi RRI LLi LLI e ai o au"""),
      'virama': [''],
      'other': s('M H .N'),
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
      "A": ["aa"], "I": ["ii"], "U": ["uu"], "RRi": ["R^i"], "RRI": ["R^I"], "LLi": ["L^i"], "LLI": ["L^I"],
      "M": [".m", ".n"], "v": ["w"], "kSh": ["x", "kS"], "j~n": ["GY"]
    }),
    IAST: Scheme({
      'vowels': s("""a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"""),
      'marks': s("""ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"""),
      'virama': [''],
      'other': s('ṃ ḥ m̐'),
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
    }),
    KANNADA: Scheme({
      'vowels': s("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ"""),
      'marks': s("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೇ ೈ ೋ ೌ"""),
      'virama': s('್'),
      'other': s('ಂ ಃ ँ'),
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
    }, is_roman=False),
    MALAYALAM: Scheme({
      'vowels': s("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ"""),
      'marks': s("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ േ ൈ ോ ൌ"""),
      'virama': s('്'),
      'other': s('ം ഃ ँ'),
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
    }, is_roman=False),
    ORIYA: Scheme({
      'vowels': s("""ଅ ଆ ଇ ଈ ଉ ଊ ଋ ୠ ଌ ୡ ଏ ଐ ଓ ଔ"""),
      'marks': ['ା', 'ି', 'ୀ', 'ୁ', 'ୂ', 'ୃ', 'ୄ',
                '', '', 'େ', 'ୈ', 'ୋ', 'ୌ'],
      'virama': s('୍'),
      'other': s('ଂ ଃ ଁ'),
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
    }, is_roman=False),
    SLP1: Scheme({
      'vowels': s("""a A i I u U f F x X e E o O"""),
      'marks': s("""A i I u U f F x X e E o O"""),
      'virama': [''],
      'other': s('M H ~'),
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
    }),
    WX: Scheme({
      'vowels': s("""a A i I u U q Q L ḹ e E o O"""),
      'marks': s("""A i I u U q Q L ḹ e E o O"""),
      'virama': [''],
      'other': s('M H ~'),
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
    }),
    TAMIL: Scheme({
      'vowels': s("""அ ஆ இ ஈ உ ஊ ऋ ॠ ऌ ॡ ஏ ஐ ஓ ஔ"""),
      'marks': ['ா', 'ி', 'ீ', 'ு', 'ூ', '', '',
                '', '', 'ே', 'ை', 'ோ', 'ௌ'],
      'virama': s('்'),
      'other': s('ஂ ஃ ँ'),
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
    }, is_roman=False),
    TELUGU: Scheme({
      'vowels': s("""అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ"""),
      'marks': s("""ా ి ీ ు ూ ృ ౄ ౢ ౣ ే ై ో ౌ"""),
      'virama': s('్'),
      'other': s('ం ః ఁ'),
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
    }, is_roman=False)
  })


_setup()


def get_approx_deduplicating_key(text, encoding_scheme=DEVANAGARI):
  """
  Given some devanAgarI sanskrit text, this function produces a "key" so
  that

  1] The key should be the same for different observed orthographical
  forms of the same text. For example:

  ::

      - "dharmma" vs "dharma"
      - "rAmaM gacChati" vs "rAma~N gacChati" vs "rAma~N gacChati"
      - "kurvan eva" vs "kurvanneva"

  2] The key should be different for different for different texts.

  -  "stamba" vs "stambha"

  This function attempts to succeed at [1] and [2] almostall the time.
  Longer the text, probability of failing at [2] decreases, while
  probability of failing at [1] increases (albeit very slightly).

  Sources of orthographically divergent forms:

  -  Phonetically sensible grammar rules
  -  Neglect of sandhi while writing
  -  Punctuation, spaces, avagraha-s.
  -  Regional-language-influenced mistakes (La instead of la.)

  Some example applications of this function:

  -  Create a database of quotes or words with minimal duplication.
  -  Search a database of quotes or words while being robust to optional
     forms.

  Also see equivalent function in the scala indic-transliteration package.
  """
  if encoding_scheme == DEVANAGARI:
    key = text
    key = regex.sub("\\P{IsDevanagari}", "", key)
    # Remove spaces
    key = regex.sub("\\s", "", key)
    # Remove punctuations
    key = regex.sub("\\p{P}", "", key)
    # Remove digits, abbreviation sign, svara-s, avagraha
    key = regex.sub("[०-९।॥॰ऽ]|[॑-॔]", "", key)
    # Collapse semi-vowel-anunAsika-s संलग्नम् सल्ँलग्नम् into m
    key = regex.sub("[यरल]्ँ", "म्", key)
    # Collapse all panchama-s into m
    key = regex.sub("[ङञणन]", "म", key)
    # Collapse anusvAra into m
    key = regex.sub("ँ|ं", "म्", key)
    key = regex.sub("ॐ", "ओम्", key)
    key = regex.sub("[ळऴ]", "ल", key)
    # Deal with optional forms where consonants are duplicated - like dharmma
    # Details in https://docs.google.com/spreadsheets/d/1GP8Ps_hmgCGLZPWKIVBCfQB9ZmPQOaCwTrH9OybaWaQ/edit#gid=21
    key = regex.sub("([क-हक़-य़])्\\1+", "\\1", key)
    key = regex.sub("[कग]्ख्", "ख्", key)
    key = regex.sub("[कग]्घ्", "घ्", key)
    key = regex.sub("च्छ्", "छ्", key)
    key = regex.sub("ज्झ्", "झ्", key)
    key = regex.sub("त्थ्", "थ्", key)
    key = regex.sub("द्ध्", "ध्", key)
    key = regex.sub("ड्ढ्", "ढ्", key)
    key = regex.sub("प्फ्", "फ्", key)
    key = regex.sub("ब्भ्", "भ्", key)
    return key
  else:
    logging.warning("got script {} for '{}'".format(encoding_scheme, text))
    return regex.sub("\\s", "", text)