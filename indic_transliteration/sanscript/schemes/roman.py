import sys

from indic_transliteration.sanscript import Scheme

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

ALL_SCHEME_IDS = [ HK,IAST, SLP1, ITRANS,WX, KOLKATA, VELTHUIS, OPTITRANS ]

s = str.split
if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences
    s = unicode.split


class RomanScheme(Scheme):
    def __init__(self, data=None, synonym_map=None, name=None):
        super(RomanScheme, self).__init__(data=data, synonym_map=synonym_map, name=name, is_roman=True)
    
    def get_standard_form(self, data):
        """Roman schemes define multiple representations of the same devanAgarI character. This method gets a library-standard representation.
        
        data : a text in the given scheme.
        """
        if self.synonym_map is None:
            return data
        from indic_transliteration import sanscript
        return sanscript.transliterate(data=sanscript.transliterate(_from=self.name, _to=sanscript.DEVANAGARI, data=data), _from=sanscript.DEVANAGARI, _to=self.name)


class ItransScheme(RomanScheme):
    def __init__(self):
        super(ItransScheme, self).__init__({
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
        }, name=ITRANS)

    def fix_lazy_anusvaara(self, data_in):
        data_out = data_in
        import regex
        data_out = regex.sub(r'M( *)([kgx])', r'~N\1\2',   data_out)
        data_out = regex.sub(r'M( *)([cCj])', r'~n\1\2',   data_out)
        data_out = regex.sub(r'M( *)([tdn])', r'n\1\2',   data_out)
        data_out = regex.sub(r'M( *)([TDN])', r'N\1\2',   data_out)
        data_out = regex.sub(r'M( *)([pb])', r'm\1\2',   data_out)
        data_out = regex.sub(r'M( *)([yvl])', r'\2.N\1\2',   data_out)
        return data_out


class OptitransScheme(RomanScheme):
    def __init__(self):
        super(OptitransScheme, self).__init__({
            'vowels': s("""a A i I u U R RR LLi LLI e ai o au E O"""),
            'marks': s("""A i I u U R RR LLi LLI e ai o au E O"""),
            'virama': [''],
            'yogavaahas': s('M H .N kH pH'),
            'consonants': s("""
                            k kh g gh ~N
                            ch Ch j jh ~n
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            sh Sh s h
                            L x jn
                            """)
                          + s("""ऩ .Rh ऴ .k q .g z .D .Dh f य़"""),
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
            "v": ["w"], "x": ["kSh", "kS", "ksh"], "jn": ["GY", "jJN", "JN"],
            "|": ["."], "||": [".."]
        }, name=OPTITRANS)

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


class IastScheme(RomanScheme):
    def __init__(self, kolkata_variant=False):
        super(IastScheme, self).__init__({
            'vowels': s("""a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au ê ô"""),
            'marks': s("""ā i ī u ū ṛ ṝ ḷ ḹ e ai o au ê ô"""),
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
                            """)
                          + s("""ṉa ṟa ḽa qa k͟ha ġa za ṛa ṛha fa ẏa"""),
            'symbols': s("""
                       oṃ ' | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, name=IAST)
        if kolkata_variant:
            self['vowels'] = s("""a ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au ê ô""")
            self['marks'] = s("""ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au ê ô""")
            self.name = KOLKATA
        self.synonym_map = {"|": ["."], "||": [".."], "'": ["`"]}
        def add_capitalized_synonyms(some_list):
            self.synonym_map.update(zip(some_list, [[x.capitalize()] for x in some_list]))
        add_capitalized_synonyms(self["vowels"])
        add_capitalized_synonyms(self["consonants"])
        add_capitalized_synonyms(["oṃ"])


class HkScheme(RomanScheme):
    def __init__(self):
        super(HkScheme, self).__init__({
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
        }, name=HK, synonym_map={"|": ["."], "||": [".."]})
        
        
class VelthiusScheme(RomanScheme):
    def __init__(self):
        super(VelthiusScheme, self).__init__({
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
        }, name=VELTHUIS)


class Slp1Scheme(RomanScheme):
    def __init__(self):
        super(Slp1Scheme, self).__init__({
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
        }, name=SLP1)
        

class WxScheme(RomanScheme):
    def __init__(self):
        super(WxScheme, self).__init__({
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
        }, name=WX, 
            # Reference for the below:
            synonym_map={"'": ["Z"], "~": ["z"]})
        

SCHEMES = {
    HK: HkScheme(),
    VELTHUIS: VelthiusScheme(),
    OPTITRANS: OptitransScheme(),
    ITRANS: ItransScheme(),
    IAST: IastScheme(),
    KOLKATA: IastScheme(kolkata_variant=True),
    SLP1: Slp1Scheme(),
    WX: WxScheme()
}