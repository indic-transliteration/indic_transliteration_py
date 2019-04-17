# Brahmi schemes
# -------------
import sys

from indic_transliteration.sanscript import Scheme


s = str.split
if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences
    s = unicode.split


class BrahmicScheme(Scheme):
    def __init__(self, data=None, synonym_map=None, name=None):
        super(BrahmicScheme, self).__init__(data=data, synonym_map=synonym_map, name=name, is_roman=False)
        self.vowel_to_mark_map = dict(zip(self["vowels"], [""] + self["marks"]))

    def do_vyanjana_svara_join(self, vyanjanaanta, svaraadi):
        import regex
        if regex.match("|".join(self['vowels']) + ".*", svaraadi):
            return vyanjanaanta[:-1] + self.vowel_to_mark_map[svaraadi[0]] + svaraadi[1:]
        else:
            raise ValueError(svaraadi + " is not svaraadi.")
