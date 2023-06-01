import os

import regex
from indic_transliteration.sanscript import Scheme
from indic_transliteration.sanscript.schemes import load_scheme
from indic_transliteration.sanscript.schemes import dev_vowel_to_mark_map

# Roman schemes
# -------------
HK = 'hk'
HK_DRAVIDIAN = 'hk_dravidian'
IAST = 'iast'
ISO = 'iso'
ISO_VEDIC = 'iso_vedic'
ITRANS = 'itrans'
ITRANS_DRAVIDIAN = 'itrans_dravidian'
TITUS = 'titus'

"""Optitransv1 is described in https://sanskrit-coders.github.io/input/optitrans/#optitrans-v1 . OPTITRANS, while staying close to ITRANS it provides a more intuitive transliteration compared to ITRANS (shankara manju - शङ्कर मञ्जु)."""
OPTITRANS = 'optitrans'
OPTITRANS_DRAVIDIAN = 'optitrans_dravidian'
KOLKATA_v2 = 'kolkata_v2'
SLP1 = 'slp1'
SLP1_ACCENTED = 'slp1_accented'
VELTHUIS = 'velthuis'
WX = 'wx'

CAPITALIZABLE_SCHEME_IDS = ["iast", "iast_iso_m", "iso", "iso_vedic", "kolkata_v2", "titus"]


class RomanScheme(Scheme):
  def __init__(self, data=None, name=None, **kwargs):
    super(RomanScheme, self).__init__(data=data, name=name, is_roman=True)
    self["vowel_marks"] = dict([(dev_vowel_to_mark_map[k], v) for k, v in self["vowels"].items() if k != "अ"])
    pass

  def get_standard_form(self, data):
    """Roman schemes define multiple representations of the same devanAgarI character. This method gets a library-standard representation.
    
    data : a text in the given scheme.
    """
    if self["alternates"] is None:
      return data
    from indic_transliteration import sanscript
    return sanscript.transliterate(data=sanscript.transliterate(_from=self.name, _to=sanscript.DEVANAGARI, data=data),
                                   _from=sanscript.DEVANAGARI, _to=self.name)

  def get_double_lettered(self, text):
    text = self.get_standard_form(data=text)
    text = text.replace("A", "aa")
    text = text.replace("I", "ii")
    text = text.replace("U", "uu")
    return text

  def mark_off_non_indic_in_line(self, text):
    words = text.split()
    from indic_transliteration import detect
    out_words = []
    for word in words:
      if detect.detect(word).lower() != self.name.lower():
        out_words.append("<%s>" % word)
      else:
        out_words.append(word)
    return " ".join(out_words)


class ItransScheme(RomanScheme):
  def fix_lazy_anusvaara(self, data_in, omit_sam=False, omit_yrl=False, ignore_padaanta=True):
    if ignore_padaanta:
      return self.fix_lazy_anusvaara_except_padaantas(data_in=data_in, omit_sam=omit_sam, omit_yrl=omit_yrl)
    data_out = data_in
    import regex
    if omit_sam:
      prefix = "(?<!sa)"
    else:
      prefix = ""
    data_out = regex.sub('%sM( *)([kgx])' % (prefix), r'~N\1\2', data_out)
    data_out = regex.sub('%sM( *)([cCj])' % (prefix), r'~n\1\2', data_out)
    data_out = regex.sub('%sM( *)([tdn])' % (prefix), r'n\1\2', data_out)
    data_out = regex.sub('%sM( *)([TDN])' % (prefix), r'N\1\2', data_out)
    data_out = regex.sub('%sM( *)([pb])' % (prefix), r'm\1\2', data_out)
    if not omit_yrl:
      data_out = regex.sub('%sM( *)([yvl])' % (prefix), r'\2.N\1\2', data_out)
    return data_out


class OptitransScheme(RomanScheme):

  def to_lay_indian(self, text, jn_replacement="GY", t_replacement="t"):
    text = self.get_standard_form(data=text)
    text = text.replace('RR', 'ri')
    text = text.replace('R', 'ri')
    text = text.replace('LLi', 'lri')
    text = text.replace('LLI', 'lri')
    text = text.replace('jn', jn_replacement)
    text = text.replace('x', 'ksh')
    if t_replacement != "t":
      text = text.replace("t", t_replacement)
    text = text.lower()
    return text

  def approximate_from_iso_urdu(self, text, add_terminal_a=True):
    # Arabic pattern = [؀-ۿ]
    # Order matters below
    replacements = {"‘": "", "ʼ": "{}", "’": "{}",
                    "oo": "uu", "ee": "ii", "ë": "E", "ě": "E", "e": "ē", "o": "ō",
                    "ā": "aa", "ī": "ii", "ū": "uu", "w": "v", 
                    "ẕ": "z", "ż": "z", "ẓ": "z", "ž": "z", "̌":"",
                    "c̱ẖ": "ć", "chh": "ćh", "ch": "c", "ć": "c", 
                    "ḳ": "q", "ṣ": "s",
                    "s̱ẖ": "sh", "s̱": "t", "ẖ": "h", "ḥ": "h", "̱": "", "̠": "", 
                    "r̤i": "r̥", "̤": ""
                    }
    for key, value in replacements.items():
      text = text.replace(key, value)
    vowels_pattern = r'[aāeēiīoōuū]'
    text = regex.sub(r"(%s)'" % vowels_pattern, r"\1", text)
    text = regex.sub(r"'(%s)" % vowels_pattern, r"\1", text)
    text = regex.sub(r"'(?=\s|$|-)", "", text)
    text = regex.sub(r"'h", "{}h", text)
    ## For remaining cases, sometimes ' should just go आस्रत|ās'rat, sometimes it represents a weak a -  आसकत|ās'kat. So we just remove it - though it makes the prior careful replacements moot. Maybe we can do something smarter in the future?
    text = text.replace("'", "")
    text = regex.sub(r"ṅ(?=[^kgq]|$)", "m̐", text)
    if add_terminal_a:
      text = regex.sub(r"([kghncjzftdTDpbmyrlvsq])(?=\s|$|-)", r"\1a", text)
    from indic_transliteration import sanscript
    text = sanscript.transliterate(text, sanscript.ISO, sanscript.OPTITRANS)
    return text


class CapitalizableScheme(RomanScheme):
  def __init__(self, data=None, is_roman=True, name=None):
    super(CapitalizableScheme, self).__init__(data=data, is_roman=is_roman, name=name)

    # A local function.
    def add_capitalized_synonyms(some_list):
      for x in some_list:
        synonyms = [x.capitalize(), x.upper()]
        if x in self["alternates"]:
          synonyms += self["alternates"][x] + [y.capitalize() for y in self["alternates"][x]] + [y.upper() for y in self["alternates"][x]]
        self["alternates"][x] = list(set(synonyms))

    add_capitalized_synonyms(self["vowels"].values())
    add_capitalized_synonyms(self["consonants"].values())
    if "extra_consonants" in self:
      add_capitalized_synonyms(self["extra_consonants"].values())
    if "accented_vowel_alternates" in self:
      add_capitalized_synonyms(self["accented_vowel_alternates"].keys())
    add_capitalized_synonyms(["oṃ"])

  def get_standard_form(self, data):
    pattern = "([%s])([̥̇¯̄]+)" % ("".join(self["accents"].values()))
    data = regex.sub(pattern, "\\2\\1", data)
    return super(CapitalizableScheme, self).get_standard_form(data=data)


SCHEMES = {}
data_path = os.path.join(os.path.dirname(__file__), "data", "roman")
for f in os.listdir(data_path):
  cls = RomanScheme
  name = f.replace(".toml", "")
  if name.startswith("optitrans"):
    cls = OptitransScheme
  elif name.startswith("itrans"):
    cls = ItransScheme
  elif name in CAPITALIZABLE_SCHEME_IDS:
    cls = CapitalizableScheme
  scheme = load_scheme(file_path=os.path.join(data_path, f), cls=cls)
  SCHEMES[scheme.name] = scheme

ALL_SCHEME_IDS = SCHEMES.keys()
