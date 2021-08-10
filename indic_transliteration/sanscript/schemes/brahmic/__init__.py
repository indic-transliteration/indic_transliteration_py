# Brahmi schemes
# -------------
import regex

from indic_transliteration.sanscript import Scheme
from indic_transliteration.sanscript.schemes import dev_vowel_to_mark_map

class BrahmicScheme(Scheme):
    def __init__(self, data=None, name=None, **kwargs):
        super(BrahmicScheme, self).__init__(data=data, name=name, is_roman=False)
        if "vowel_marks" in self:
            self.vowel_to_mark_map = {}
            for (vowel, vowel_mark) in dev_vowel_to_mark_map.items():
                if vowel in self["vowels"] and vowel_mark in self["vowel_marks"]:
                    self.vowel_to_mark_map[self["vowels"][vowel]] = self["vowel_marks"][vowel_mark]

    def do_vyanjana_svara_join(self, vyanjanaanta, svaraadi):
        import regex
        if regex.match("|".join(self['vowels']) + ".*", svaraadi):
            return vyanjanaanta[:-1] + self.vowel_to_mark_map[svaraadi[0]] + svaraadi[1:]
        else:
            raise ValueError(svaraadi + " is not svaraadi.")

    def apply_roman_numerals(self, in_string):
        out_string = in_string
        dev_numerals = "० १ २ ३ ४ ५ ६ ७ ८ ९".split()
        for k, v in self['symbols'].items():
            if k >= "०" and k <= "९":
                numeral = dev_numerals.index(k)
                out_string = out_string.replace(self['symbols'][k], str(numeral))
        return out_string
    
    def remove_svaras(self, in_string):
      out_string = regex.sub(r"[॑-॔᳐-᳨᳸᳹꣠-꣱]", "", in_string)
      out_string = out_string.replace("ꣳ", "ं")
      return out_string

    def remove_punctuation(self, in_string):
        return regex.sub(r"[.।॥]", "", in_string)



class DevanagariScheme(BrahmicScheme):

    @classmethod
    def fix_lazy_visarga(cls, data_in):
        data_out = data_in
        import regex
        data_out = regex.sub(r'ः( *)([क-ङ])', r'ᳵ\1\2',   data_out)
        data_out = regex.sub(r'ः( *)([प-म])', r'ᳶ\1\2',   data_out)
        return data_out

    def fix_lazy_anusvaara(self, data_in, omit_sam=False, omit_yrl=False, ignore_padaanta=False):
        # Overriding because we don't want to turn जगइ to जगै
        if ignore_padaanta:
            return self.fix_lazy_anusvaara_except_padaantas(data_in=data_in, omit_sam=omit_sam, omit_yrl=omit_yrl)
        data_out = data_in
        import regex
        if omit_sam:
            prefix = "(?<!स)"
        else:
            prefix = ""
        data_out = regex.sub('%sं( *)([क-ङ])' % (prefix), r'ङ्\1\2',   data_out)
        data_out = regex.sub('%sं( *)([च-ञ])' % (prefix), r'ञ्\1\2',   data_out)
        data_out = regex.sub('%sं( *)([त-न])' % (prefix), r'न्\1\2',   data_out)
        data_out = regex.sub('%sं( *)([ट-ण])' % (prefix), r'ण्\1\2',   data_out)
        data_out = regex.sub('%sं( *)([प-म])' % (prefix), r'म्\1\2',   data_out)
        data_out = regex.sub('ं$', r'म्',   data_out)
        if not omit_yrl:
            data_out = regex.sub('%sं( *)([यलव])' % (prefix), r'\2्ँ\1\2',   data_out)
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


DEVANAGARI = 'devanagari'
GUJARATI = 'gujarati'
GURMUKHI = 'gurmukhi'
GUNJALA_GONDI = 'gondi_gunjala'
BENGALI = 'bengali'
ORIYA = 'oriya'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TAMIL = 'tamil'
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
    scheme = load_scheme(file_path=os.path.join(data_path, f), cls=cls)
    SCHEMES[scheme.name] = scheme