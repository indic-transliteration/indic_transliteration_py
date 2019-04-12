# -*- coding: utf-8 -*-
"""
Some useful functions for converting and disambiguating between common alternative orthographies (ways of writing) the same text.
"""

import logging

# Not using the more standard library re here : We need to support `key = re.sub("\\P{IsDevanagari}", "", key)`.
import regex
from indic_transliteration import sanscript


def get_approx_deduplicating_key(text, encoding_scheme=sanscript.DEVANAGARI):
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
    if encoding_scheme == sanscript.DEVANAGARI:
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
