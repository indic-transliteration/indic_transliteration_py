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

  SCHEMES = copy.deepcopy(sanscript.SCHEMES)
  for scheme in [sanscript.ORIYA, sanscript.BENGALI, sanscript.GUJARATI]:
    SCHEMES.pop(scheme)
  SCHEMES[DEVANAGARI].update({
      'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ऎ ए ऐ ऒ ओ औ"""),
      'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ ॆ े ै ॊ ो ौ"""),
      'consonants': s("""
                            क ख ग घ ङ
                            च छ ज झ ञ
                            ट ठ ड ढ ण
                            त थ द ध न
                            प फ ब भ म
                            य र ल व
                            श ष स ह
                            ळ क्ष ज्ञ
                            ऩ ऱ ऴ
                            """)})
  SCHEMES[HK].update({
      'vowels': s("""a A i I u U R RR lR lRR e E ai o O au"""),
      'marks': s("""A i I u U R RR lR lRR e E ai o O au"""),
      'consonants': s("""
                            k kh g gh G
                            c ch j jh J
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            z S s h
                            L kS jJ
                            n2 r2 zh
                            """),
    })
  SCHEMES[ITRANS].update({
      'vowels': s("""a A i I u U RRi RRI LLi LLI e E ai o O au"""),
      'marks': s("""A i I u U RRi RRI LLi LLI e E ai o O au"""),
      'consonants': s("""
                            k kh g gh ~N
                            ch Ch j jh ~n
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            sh Sh s h
                            L kSh j~n
                            .n .R .L
                            """),
    })
  SCHEMES[IAST].update({
      'vowels': s("""a ā i ī u ū ṛ ṝ ḷ ḹ ê e ai ô o au"""),
      'marks': s("""ā i ī u ū ṛ ṝ ḷ ḹ ê e ai ô o au"""),
      'consonants': s("""
                            k kh g gh ṅ
                            c ch j jh ñ
                            ṭ ṭh ḍ ḍh ṇ
                            t th d dh n
                            p ph b bh m
                            y r l v
                            ś ṣ s h
                            ḻ kṣ jñ
                            n r̂ ḷ
                            """),
    })
  SCHEMES[KANNADA].update({
      'vowels': s("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಎ ಏ ಐ ಒ ಓ ಔ"""),
      'marks': s("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೆ ೇ ೈ ೊ ೋ ೌ"""),
      'consonants': s("""
                            ಕ ಖ ಗ ಘ ಙ
                            ಚ ಛ ಜ ಝ ಞ
                            ಟ ಠ ಡ ಢ ಣ
                            ತ ಥ ದ ಧ ನ
                            ಪ ಫ ಬ ಭ ಮ
                            ಯ ರ ಲ ವ
                            ಶ ಷ ಸ ಹ
                            ಳ ಕ್ಷ ಜ್ಞ
                            ऩ ಱ ೞ
                            """),
    })
  SCHEMES[MALAYALAM].update({
      'vowels': s("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ എ ഏ ഐ ഓ ഒ ഔ"""),
      'marks': s("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ െ േ ൈ ൊ ോ ൌ"""),
      'consonants': s("""
                            ക ഖ ഗ ഘ ങ
                            ച ഛ ജ ഝ ഞ
                            ട ഠ ഡ ഢ ണ
                            ത ഥ ദ ധ ന
                            പ ഫ ബ ഭ മ
                            യ ര ല വ
                            ശ ഷ സ ഹ
                            ള ക്ഷ ജ്ഞ
                            ऩ ള ൟ
                            """),
    })
  SCHEMES[TAMIL].update({
      'vowels': s("""அ ஆ இ ஈ உ ஊ ऋ ॠ ऌ ॡ எ ஏ ஐ ஒ ஓ ஔ"""),
      'marks': ['ா', 'ி', 'ீ', 'ு', 'ூ', '', '',
                '', '', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ'],
      'consonants': s("""
                            க க க க ங
                            ச ச ஜ ச ஞ
                            ட ட ட ட ண
                            த த த த ந
                            ப ப ப ப ம
                            ய ர ல வ
                            ஶ ஷ ஸ ஹ
                            ள க்ஷ ஜ்ஞ
                            ன ற ழ 
                            """)
    })
  SCHEMES[TELUGU].update({
      'vowels': s("""అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఎ ఏ ఐ ఒ ఓ ఔ"""),
      'marks': s("""ా ి ీ ు ూ ృ ౄ ౢ ౣ 
ె ే ై ొ ో ౌ"""),
      'consonants': s("""
                            క ఖ గ ఘ ఙ
                            చ ఛ జ ఝ ఞ
                            ట ఠ డ ఢ ణ
                            త థ ద ధ న
                            ప ఫ బ భ మ
                            య ర ల వ
                            శ ష స హ
                            ళ క్ష జ్ఞ
                            ऩ ఴ ౚ
                            """),
      'symbols': s("""
                       ఓం ఽ । ॥
                       ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯
                       """)
    })



_setup()
