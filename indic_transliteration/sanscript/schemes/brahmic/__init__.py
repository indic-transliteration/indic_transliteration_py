# Brahmi schemes
# -------------
import regex

from indic_transliteration.sanscript import Scheme
from indic_transliteration.sanscript.schemes import dev_vowel_to_mark_map
from functools import reduce


class BrahmicScheme(Scheme):
  ACCENTS = "[\u1CD0-\u1CE8\u1CF9\u1CFA\uA8E0-\uA8F1\u0951-\u0954\u0957]" # included  ॗ , which is used as svara for weber's shatapatha
  YOGAVAAHAS = "[\u0900-\u0903\uA8F2-\uA8F7ᳩ-ᳶ]"
  def __init__(self, data=None, name=None, **kwargs):
    super(BrahmicScheme, self).__init__(data=data, name=name, is_roman=False)
    if "vowel_marks" in self:
      self.vowel_to_mark_map = {}
      self.mark_to_vowel_map = {}
      for (vowel, vowel_mark) in dev_vowel_to_mark_map.items():
        if vowel in self["vowels"] and vowel_mark in self["vowel_marks"]:
          self.vowel_to_mark_map[self["vowels"][vowel]] = self["vowel_marks"][vowel_mark]
          self.mark_to_vowel_map[self["vowel_marks"][vowel_mark]] = self["vowels"][vowel]

      self.long_vowel_marks = [self.vowel_to_mark_map[x] for x in self.long_vowels]


  def do_vyanjana_svara_join(self, vyanjanaanta, svaraadi):
    import regex
    if regex.match("|".join(self['vowels'].values()) + ".*", svaraadi):
      if len(svaraadi) > 1:
        remainder = svaraadi[1:]
      else:
        remainder = ""
      return vyanjanaanta[:-1] + self.vowel_to_mark_map.get(svaraadi[0], "") + remainder
    else:
      raise ValueError(svaraadi + " is not svaraadi.")

  def split_vyanjanas_and_svaras(self, text):
    def _yogavaaha_accent_match(letter):
      return letter in self["yogavaahas"].values() or letter in self.get("accents", {}).values() or regex.match(self.YOGAVAAHAS, letter) or regex.match(self.ACCENTS, letter) is not None or letter in self.get("candra", {}).values()
    
    letters = []
    for letter in text:
      if letter in self.mark_to_vowel_map:
        if len(letters) > 0:
          letters[-1] += self["virama"]["्"]
        letters.append(self.mark_to_vowel_map[letter])
      elif _yogavaaha_accent_match(letter) or letter in self[
        "virama"].values():
        if len(letters) > 0:
          letters[-1] += letter
        else:
          letters.append(letter)
      else:
        letters.append(letter)
    out_letters = []
    for letter in letters:
      if letter in self["consonants"].values() or letter in self.get("extra_consonants", {}).values():
        out_letters.append(letter)
        out_letters[-1] += self["virama"]["्"]
        out_letters.append(self["vowels"]["अ"])
      elif (letter[0] in self["consonants"].values() or letter[0] in self.get("extra_consonants", {}).values()) and (_yogavaaha_accent_match(letter[1]) or _yogavaaha_accent_match(letter[-1])):
        out_letters.append(letter[0])
        out_letters[-1] += self["virama"]["्"]
        out_letters.append(self["vowels"]["अ"] + letter[-1])      
      else:
        out_letters.append(letter)
    return out_letters

  def get_consonant_letters(self, text):
    letters = self.split_vyanjanas_and_svaras(text)
    letters = [letter.replace(self["virama"]["्"], "") for letter in letters if letter.replace(self["virama"]["्"], "") in self["consonants"].values()]
    return letters

  def join_post_viraama(self, text):
    VIRAMA = self["virama"]["्"]
    VOWELS = "".join(self["vowels"].values())
    text_out = text
    # regex.sub replaces only non-overlapping strings. Hence:
    for match in regex.finditer(rf"(.{VIRAMA})[\s-]*(\S)", text_out, overlapped=True):
      text_out = text_out.replace(match.group(), self.join_strings([match.group(1), match.group(2)]))
    text_out = regex.sub("[\s-]*ऽ", "ऽ", text_out)
    text_out = regex.sub("-", "", text_out)
    return text_out

  def join_strings(self, strings):
    out_text = ""
    for letter in strings:
      if letter[0] in self["vowels"].values() and out_text.endswith(self["virama"]["्"]):
        out_text = out_text[:-1] + self.vowel_to_mark_map.get(letter[0], "")
        if len(letter) > 1:
          out_text += letter[1:]
      else:
        out_text = out_text + letter
    return out_text

  def get_numerals(self):
    dev_numerals = "० १ २ ३ ४ ५ ६ ७ ८ ९".split()
    return [self["symbols"][x] for x in dev_numerals]

  def apply_roman_numerals(self, in_string):
    out_string = in_string
    native_numerals = self.get_numerals()
    for numeral, native_numeral in enumerate(native_numerals):
      out_string = out_string.replace(str(native_numeral), str(numeral))
    return out_string

  def remove_svaras(self, in_string):
    SVARAS = r"[\u1CD0-\u1CE8\u1CF9\u1CFA\uA8E0-\uA8F1\u0951-\u0954\u0957]"
    out_string = regex.sub(f"[१३]{SVARAS}+", "", in_string)
    out_string = regex.sub(SVARAS, "", out_string)
    out_string = out_string.replace("ꣳ", "ं")
    return out_string

  def remove_punctuation(self, in_string):
    return regex.sub(r"[.।॥:-]", "", in_string)

  def remove_numerals(self, in_string):
    native_numerals = self.get_numerals()
    return regex.sub(r"[%s\d]" % "".join(native_numerals), "", in_string)

  def dot_for_numeric_ids(self, in_string):
    native_numerals = self.get_numerals()
    native_numerals_pattern = "[%s\d]" % "".join(native_numerals)
    return regex.sub(r"(%s)।(?=%s)" % (native_numerals_pattern, native_numerals_pattern), "\\1.", in_string)

  def get_letters(self):
    letters = list(self["vowels"].values()) + list(self["consonants"].values()) + list(self["vowel_marks"].values()) + list(self[
      "yogavaahas"].values()) + list(self["virama"].values()) + list(self["extra_consonants"].values()) + [self["symbols"]["ॐ"]] + reduce(
      lambda x, y: x + y, list(self["alternates"].values()))
    return letters


class DevanagariScheme(BrahmicScheme):
  PATTERN_CONSONANT_MODIFIER = "़्"
  PATTERN_YOGAVAAHA = r"ऀ-ःᳩ-ᳶ"
  PATTERN_GURU_YOGAVAAHA = r"ंःᳩ-ᳶ"
  PATTERN_ACCENT = r"॑-॔\uA8E0-꣼\u1CD0-\u1CFF"
  PATTERN_DEPENDENT_VOWEL = r"\u093A-\u093B\u093E-\u094C \u094E-\u094F\u0955-\u0957\u0962-\u0963\uA8FF"
  PATTERN_GURU_DEPENDENT_VOWEL = r"ऻ ा ी ू ॄ ॗॣ ॎ े ै ो ौ ॕ".replace(" ", "")
  PATTERN_GURU_INDEPENDENT_VOWEL = "आईऊॠॡएऐओऔऍऑॴॵॷꣾ"
  PATTERN_VYANJANA = "क-हक़-य़ॸ-ॿ"
  PATTERN_VYANJANA_WITHOUT_VOWEL = "[%s]़?्" % (PATTERN_VYANJANA)
  PATTERN_INDEPENDENT_VOWEL = "ऄ-औॠॡॲ-ॷꣾ"
  PATTERN_OM = "ॐꣽ"

  @classmethod
  def fix_lazy_visarga(cls, data_in):
    data_out = data_in
    import regex
    data_out = regex.sub(r'ः( *)([क-ङ])', r'ᳵ\1\2', data_out)
    data_out = regex.sub(r'ः( *)([प-म])', r'ᳶ\1\2', data_out)
    return data_out

  def fix_lazy_anusvaara(self, data_in, omit_sam=False, omit_yrl=False, ignore_padaanta=True):
    # Overriding because we don't want to turn जगइ to जगै
    if ignore_padaanta:
      return self.fix_lazy_anusvaara_except_padaantas(data_in=data_in, omit_sam=omit_sam, omit_yrl=omit_yrl)
    data_out = data_in
    import regex
    if omit_sam:
      prefix = "(?<!स)"
    else:
      prefix = ""
    data_out = regex.sub("ंऽ", "ऽं", data_out)
    data_out = regex.sub('%sं( *)([क-ङ])' % (prefix), r'ङ्\1\2', data_out)
    data_out = regex.sub('%sं( *)([च-ञ])' % (prefix), r'ञ्\1\2', data_out)
    data_out = regex.sub('%sं( *)([त-न])' % (prefix), r'न्\1\2', data_out)
    data_out = regex.sub('%sं( *)([ट-ण])' % (prefix), r'ण्\1\2', data_out)
    data_out = regex.sub('%sं( *)([प-म])' % (prefix), r'म्\1\2', data_out)
    data_out = regex.sub('ं$', r'म्', data_out)
    if not omit_yrl:
      data_out = regex.sub('%sं( *)([यलव])' % (prefix), r'\2्ँ\1\2', data_out)
    return data_out

  def force_lazy_anusvaara(self, data_in):
    # Overriding because we don't want to turn जगइ to जगै
    data_out = data_in
    import regex
    prefix = ""
    data_out = regex.sub('ङ्( *)([क-ङ])', r'ं\1\2', data_out)
    data_out = regex.sub('ञ्( *)([च-ञ])', r'ं\1\2', data_out)
    data_out = regex.sub('न्( *)([त-न])', r'ं\1\2', data_out)
    data_out = regex.sub('ण्( *)([ट-ण])', r'ं\1\2', data_out)
    data_out = regex.sub('म्( *)([प-म])', r'ं\1\2', data_out)
    data_out = regex.sub('ं$', r'म्', data_out)
    data_out = regex.sub('[यलव]्ँ( *)([यलव])', r'ं\1\2', data_out)
    return data_out


class GurmukhiScheme(BrahmicScheme):

  @classmethod
  def replace_addak(cls, text):
    import regex
    text = regex.sub("ੱ([ਕਖ])", r"ਕ੍\g<1>", text, flags=regex.UNICODE)
    text = regex.sub(r"ੱ([ਗਘ])", r"ਗ੍\g<1>", text)
    text = regex.sub("ੱ([ਚਛ])", r"ਚ੍\g<1>", text)
    text = regex.sub("ੱ([ਜਝ])", r"ਜ੍\g<1>", text)
    text = regex.sub("ੱ([ਟਠ])", r"ਟ੍\g<1>", text)
    text = regex.sub("ੱ([ਡਢ])", r"ਡ੍\g<1>", text)
    text = regex.sub("ੱ([ਤਥ])", r"ਤ੍\g<1>", text)
    text = regex.sub("ੱ([ਦਧ])", r"ਦ੍\g<1>", text)
    text = regex.sub("ੱ([ਪਫ])", r"ਪ੍\g<1>", text)
    text = regex.sub("ੱ([ਬਭ])", r"ਬ੍\g<1>", text)
    text = regex.sub("ੱ([ਯਰਲਵਸ਼ਸਹਙਞਣਨਮਜ਼ੜਫ਼])", r"\g<1>੍\g<1>", text)
    return text

class TamilScheme(BrahmicScheme):
  @classmethod
  def move_before_maatraa_subscripts(cls, text):
    import regex
    text = regex.sub("([ா-ௌ꞉ம்]+)([₂₃₄])", r"\g<2>\g<1>", text, flags=regex.UNICODE)
    return text

  @classmethod
  def move_before_maatraa_superscripts(cls, text):
    import regex
    text = regex.sub("([ா-ௌ꞉ம்]+)([²³⁴])", r"\g<2>\g<1>", text, flags=regex.UNICODE)
    return text

  @classmethod
  def transliterate_subscripted(cls, text, _to):
    import regex
    from indic_transliteration import sanscript
    text = regex.sub("\S+[₂₃₄]\S*", lambda x: sanscript.transliterate(x.group(), _from=sanscript.TAMIL_SUB, _to=_to), text)
    return text

  @classmethod
  def transliterate_supercripted(cls, text, _to):
    import regex
    from indic_transliteration import sanscript
    text = regex.sub("\S+[²³⁴]\S*", lambda x: sanscript.transliterate(x, _from=sanscript.TAMIL_SUP, _to=_to), text)
    return text


DEVANAGARI = 'devanagari'
GUJARATI = 'gujarati'
GURMUKHI = 'gurmukhi'
GUNJALA_GONDI = 'gondi_gunjala'
BENGALI = 'bengali'
ORIYA = 'oriya'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TAMIL = 'tamil'
TAMIL_SUP = 'tamil_superscripted'
TAMIL_SUB = 'tamil_subscripted'
GRANTHA = 'grantha'
TELUGU = 'telugu'
SCHEMES = {
}

import os.path

from indic_transliteration.sanscript.schemes import load_scheme

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "brahmic")
for f in os.listdir(data_path):
  cls = BrahmicScheme
  if f.startswith("devanagari"):
    cls = DevanagariScheme
  elif f.startswith("gurmukhi"):
    cls = GurmukhiScheme
  elif f.startswith("tamil"):
    cls = TamilScheme
  scheme = load_scheme(file_path=os.path.join(data_path, f), cls=cls)
  SCHEMES[scheme.name] = scheme
