import itertools
import os
import os.path
import regex
import toml

dev_vowel_to_mark_map = toml.load(os.path.join(os.path.dirname(__file__), "data/_devanagari_vowel_to_marks.toml"))


class Scheme(dict):
  """Represents all of the data associated with a given scheme. In addition
  to storing whether or not a scheme is roman, :class:`Scheme` partitions
  a scheme's characters into important functional groups.

  :class:`Scheme` is just a subclass of :class:`dict`.

  :param data: a :class:`dict` of initial values. Note that the particular characters present here are also assumed to be the _preferred_ transliterations when transliterating to this scheme. 
  
  Among other things, data contains 'alternates': A map from keys appearing in `data` to lists of symbols with equal meaning. For example: M -> ['.n', .'m'] in ITRANS. This alternates is not used in transliterating to this scheme.
  :param is_roman: `True` if the scheme is a romanization and `False`
                   otherwise.
  """

  def __init__(self, data=None, is_roman=True, name=None):
    super(Scheme, self).__init__(data or {})
    self.is_roman = is_roman
    self.name = name

  def fix_om(self, data_in):
    replacement_pattern = "(?<=(^|\s|\p{Punct}))%s(%s|%s)(?=(\s|$|\p{Punct}))" % (self["vowels"]["ओ"], self["yogavaahas"]["ं"], self["consonants"]["म"] + self["virama"]["्"])
    return regex.sub(replacement_pattern, self["symbols"]["ॐ"], data_in)

  def apply_shortcuts(self, data_in):
    if "shortcuts" in self:
      for key, shortcut in self["shortcuts"].items():
        if key in shortcut:
          # An actually long "Shortcut" may already exist in the data
          data_in = data_in.replace(shortcut, key)
        data_in = data_in.replace(key, shortcut)
    return data_in

  def unapply_shortcuts(self, data_in):
    if "shortcuts" in self:
      for key, shortcut in self["shortcuts"].items():
        if shortcut in key:
          # An actually long "key" may already exist in the data
          data_in = data_in.replace(key, shortcut)
        data_in = data_in.replace(shortcut, key)
    return data_in

  def fix_lazy_anusvaara_except_padaantas(self, data_in, omit_sam, omit_yrl):
    lines = data_in.split("\n")
    lines_out = []
    for line in lines:
      initial_space = "".join(itertools.takewhile(str.isspace, line))
      final_space = "".join(itertools.takewhile(str.isspace, line[::-1]))
      words = line.split()
      ## We don't want ग्रामं गच्छ to turn into ग्रामङ् गच्छ or ग्रामम् गच्छ 
      fixed_words = []
      for word in words:
        if word[-1] == "ं": 
          fixed_words.append(self.fix_lazy_anusvaara(word[:-1], omit_sam=omit_sam, omit_yrl=omit_yrl, ignore_padaanta=False) + word[-1])
        else:
          fixed_words.append(self.fix_lazy_anusvaara(word, omit_sam=omit_sam, omit_yrl=omit_yrl, ignore_padaanta=False))
      lines_out.append("%s%s%s" % (initial_space, " ".join(fixed_words), final_space))
    return "\n".join(lines_out)

  def fix_lazy_anusvaara(self, data_in, omit_sam=False, omit_yrl=False, ignore_padaanta=True):
    """
    Assumption: space and newlines are the word delimiters.
    
    :param data_in: 
    :param omit_sam: 
    :param omit_yrl: 
    :param ignore_padaanta: 
    :return: 
    """
    from indic_transliteration import sanscript
    if ignore_padaanta:
      return self.fix_lazy_anusvaara_except_padaantas(data_in=data_in, omit_sam=omit_sam, omit_yrl=omit_yrl)
    data_out = sanscript.transliterate(data=data_in, _from=self.name, _to=sanscript.DEVANAGARI)
    data_out = sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara(data_in=data_out, omit_sam=omit_sam,
                                                                          omit_yrl=omit_yrl)
    return sanscript.transliterate(data=data_out, _from=sanscript.DEVANAGARI, _to=self.name)

  def replace_terminal_anusvaara(self, data_in):
    from indic_transliteration import sanscript
    data_out = sanscript.transliterate(data=data_in, _from=self.name, _to=sanscript.DEVANAGARI)
    if data_out.endswith("ं"):
      data_out = data_out[:-1] + "म्"
      return sanscript.transliterate(data=data_out, _from=sanscript.DEVANAGARI, _to=self.name)
    else:
      return data_in

  def force_lazy_anusvaara(self, data_in):
    from indic_transliteration import sanscript
    data_out = sanscript.transliterate(data=data_in, _from=self.name, _to=sanscript.DEVANAGARI)
    data_out = sanscript.SCHEMES[sanscript.DEVANAGARI].force_lazy_anusvaara(data_in=data_out)
    return sanscript.transliterate(data=data_out, _from=sanscript.DEVANAGARI, _to=self.name)

  def from_devanagari(self, data):
    """A convenience method"""
    from indic_transliteration import sanscript
    return sanscript.transliterate(data=data, _from=sanscript.DEVANAGARI, _to=self.name)


def load_scheme(file_path, cls, **kwargs):
  import codecs
  is_roman = "roman" in file_path
  name = os.path.basename(file_path).replace(".toml", "")

  def scheme_maker(data):
    if "vowels" not in data:
      return data
    return cls(data=data, name=name, is_roman=is_roman, **kwargs)

  with codecs.open(file_path, "r", 'utf-8') as file_out:
    scheme_map = toml.load(file_out)
    scheme = scheme_maker(data=scheme_map)
    return scheme
