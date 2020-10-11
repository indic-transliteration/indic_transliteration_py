import regex

from indic_transliteration.sanscript import Scheme

# Roman schemes
# -------------
HK = 'hk'
IAST = 'iast'
ITRANS = 'itrans'
TITUS = 'titus'

"""Optitransv1 is described in https://sanskrit-coders.github.io/site/pages/input/optitrans.html#optitrans-v1 . OPTITRANS, while staying close to ITRANS it provides a more intuitive transliteration compared to ITRANS (shankara manju - शङ्कर मञ्जु)."""
OPTITRANS = 'optitrans'
KOLKATA = 'kolkata'
SLP1 = 'slp1'
VELTHUIS = 'velthuis'
WX = 'wx'


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

    @classmethod
    def simplify_accent_notation(cls, text):
        # References: https://en.wikipedia.org/wiki/Combining_Diacritical_Marks
        text = text.replace("á", "á")
        text = text.replace("í", "í")
        text = text.replace("ú", "ú")
        text = text.replace("ŕ", "ŕ")
        text = text.replace("é", "é")
        text = text.replace("ó", "ó")

        text = text.replace("à", "à")
        text = text.replace("ì", "ì")
        text = text.replace("ù", "ù")
        text = text.replace("è", "è")
        text = text.replace("ò", "ò")
        
        text = regex.sub("([̀́])([̥̇¯̄]+)", "\\2\\1", text)
        return text

    @classmethod
    def to_shatapatha_svara(cls, text):
        # References: https://en.wikipedia.org/wiki/Combining_Diacritical_Marks
        text = text.replace("́", "᳘")
        text = text.replace("̀", "᳘")
        text = regex.sub("᳘([ंःँ])", "\\1᳘", text)
        return text

    def get_double_lettered(self, text):
        text = self.get_standard_form(data=text)
        text = text.replace("A", "aa")
        text = text.replace("I", "ii")
        text = text.replace("U", "uu")
        return text


class ItransScheme(RomanScheme):
    def __init__(self):
        super(ItransScheme, self).__init__({
            'vowels': str.split("""a A i I u U RRi RRI LLi LLI e ai o au"""),
            'marks': str.split("""A i I u U RRi RRI LLi LLI e ai o au"""),
            'virama': [''],
            'yogavaahas': str.split('M H .N'),
            'consonants': str.split("""
                            k kh g gh ~N
                            ch Ch j jh ~n
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            sh Sh s h
                            L kSh j~n
                            """)
                          + str.split("""n2 r2 zh q K G z .D .Dh f य़"""),
            'symbols': str.split("""
                       OM .a | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, synonym_map={
            "A": ["aa"], "I": ["ii"], "U": ["uu"], "e": ["E"], "o": ["O"], "RRi": ["R^i"], "RRI": ["R^I"], "LLi": ["L^i"], "LLI": ["L^I"],
            "M": [".m", ".n"], "v": ["w"], "kSh": ["x", "kS"], "j~n": ["GY", "jJN"],
            "||": [".."], "|": ["."]
        }, name=ITRANS)

    def fix_lazy_anusvaara(self, data_in, omit_sam=False, omit_yrl=False, ignore_padaanta=False):
        if ignore_padaanta:
            return self.fix_lazy_anusvaara_except_padaantas(data_in=data_in, omit_sam=omit_sam, omit_yrl=omit_yrl)
        data_out = data_in
        import regex
        if omit_sam:
            prefix = "(?<!sa)"
        else:
            prefix = ""
        data_out = regex.sub('%sM( *)([kgx])' % (prefix), r'~N\1\2',   data_out)
        data_out = regex.sub('%sM( *)([cCj])' % (prefix), r'~n\1\2', data_out)
        data_out = regex.sub('%sM( *)([tdn])' % (prefix), r'n\1\2', data_out)
        data_out = regex.sub('%sM( *)([TDN])' % (prefix), r'N\1\2', data_out)
        data_out = regex.sub('%sM( *)([pb])' % (prefix), r'm\1\2', data_out)
        if not omit_yrl:
            data_out = regex.sub('%sM( *)([yvl])' % (prefix), r'\2.N\1\2', data_out)
        return data_out


class OptitransScheme(RomanScheme):
    def __init__(self):
        super(OptitransScheme, self).__init__({
            'vowels': str.split("""a A i I u U R RR LLi LLI e ai o au E O"""),
            'marks': str.split("""A i I u U R RR LLi LLI e ai o au E O"""),
            'virama': [''],
            'yogavaahas': str.split('M H .N kH pH'),
            'consonants': str.split("""
                            k kh g gh ~N
                            ch Ch j jh ~n
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            sh Sh s h
                            L x jn
                            """)
                          + str.split("""ऩ .Rh .L .k q .g z .D .Dh f य़"""),
            # All those special conversions like nk -> ङ्क् are hard-coded when this scheme definition is consumed to produce a scheme map. Hence, they don't show up here.
            'symbols': str.split("""
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
            'vowels': str.split("""a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au ê ô"""),
            'marks': str.split("""ā i ī u ū ṛ ṝ ḷ ḹ e ai o au ê ô"""),
            'virama': [''],
            'yogavaahas': str.split('ṃ ḥ m̐'),
            'consonants': str.split("""
                            k kh g gh ṅ
                            c ch j jh ñ
                            ṭ ṭh ḍ ḍh ṇ
                            t th d dh n
                            p ph b bh m
                            y r l v
                            ś ṣ s h
                            ḻ kṣ jñ
                            """)
                          + str.split("""ṉ r̂ ḽ q k͟h ġ z f ẏ"""),
            'symbols': str.split("""
                       oṃ ' | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, name=IAST)
        if kolkata_variant:
            self['vowels'] = str.split("""a ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au ê ô""")
            self['marks'] = str.split("""ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au ê ô""")
            self.name = KOLKATA
        self.synonym_map = {
            "|": [".", "/"], "||": ["..", "//"], "'": ["`"],
            "m̐": ["ṁ"],
            "ṛ": ["r̥"], "ṝ": ["ṝ", "r̥̄", "r̥̄"]
        }
        
        # A local function.
        def add_capitalized_synonyms(some_list):
            for x in some_list:
                synonyms = [x.capitalize()]
                if x in self.synonym_map:
                    synonyms = self.synonym_map[x] + [y.capitalize() for y in self.synonym_map[x]]
                self.synonym_map[x] = synonyms
        add_capitalized_synonyms(self["vowels"])
        add_capitalized_synonyms(self["consonants"])
        add_capitalized_synonyms(["oṃ"])


class HkScheme(RomanScheme):
    def __init__(self):
        super(HkScheme, self).__init__({
            'vowels': str.split("""a A i I u U R RR lR lRR e ai o au"""),
            'marks': str.split("""A i I u U R RR lR lRR e ai o au"""),
            'virama': [''],
            'yogavaahas': str.split('M H ~'),
            'consonants': str.split("""
                            k kh g gh G
                            c ch j jh J
                            T Th D Dh N
                            t th d dh n
                            p ph b bh m
                            y r l v
                            z S s h
                            L kS jJ
                            """),
            'symbols': str.split("""
                       OM ' | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, name=HK, synonym_map={"|": ["."], "||": [".."]})


iast_scheme = IastScheme()


class TitusScheme(RomanScheme):
    def __init__(self):
        super(TitusScheme, self).__init__({
            'vowels': str.split("""a ā i ī u ū r̥ r̥̄ l̥ l̥̄ e ai o au"""),
            'marks': str.split("""ā i ī u ū r̥ r̥̄ l̥ l̥̄ e ai o au"""),
            'virama': [''],
            'yogavaahas': iast_scheme['yogavaahas'],
            'consonants': str.split("""
                            k kʰ g gʰ ṅ
                            c cʰ j jʰ ñ
                            ṭ ṭʰ ḍ ḍʰ ṇ
                            t tʰ d dʰ n
                            p pʰ b bʰ m
                            y r l v
                            ś ṣ s h
                            ḷ kṣ jñ
                            """),
            'symbols': str.split("""
                       oṃ ' . ..
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, name=TITUS, synonym_map={
            "m̐": ["ṁ"], 
            "r̥": ["ṛ"], "r̥̄": ["ṝ", "ṝ", "r̥̄"], "oṃ": ["ŏṃ"],
            ".": ["|", "/"], "..": ["||", "//"]
        })


class VelthiusScheme(RomanScheme):
    def __init__(self):
        super(VelthiusScheme, self).__init__({
            'vowels': str.split("""a aa i ii u uu .r .rr .l .ll e ai o au"""),
            'marks': str.split("""aa i ii u uu .r .rr .l .ll e ai o au"""),
            'virama': [''],
            'yogavaahas': str.split('.m .h /'),
            'consonants': str.split("""
                            k kh g gh "n
                            c ch j jh ~n
                            .t .th .d .dh .n
                            t th d dh n
                            p ph b bh m
                            y r l v
                            "s .s s h
                            L k.s j~n
                            """),
            'symbols': str.split("""
                       O .a | ||
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, name=VELTHUIS)


class Slp1Scheme(RomanScheme):
    def __init__(self):
        super(Slp1Scheme, self).__init__({
            'vowels': str.split("""a A i I u U f F x X e E o O"""),
            'marks': str.split("""A i I u U f F x X e E o O"""),
            'virama': [''],
            'yogavaahas': str.split('M H ~'),
            'consonants': str.split("""
                            k K g G N
                            c C j J Y
                            w W q Q R
                            t T d D n
                            p P b B m
                            y r l v
                            S z s h
                            L kz jY
                            """),
            'symbols': str.split("""
                       oM ' . ..
                       0 1 2 3 4 5 6 7 8 9
                       """)
        }, name=SLP1)
        

class WxScheme(RomanScheme):
    def __init__(self):
        super(WxScheme, self).__init__({
            'vowels': str.split("""a A i I u U q Q L ḹ e E o O"""),
            'marks': str.split("""A i I u U q Q L ḹ e E o O"""),
            'virama': [''],
            'yogavaahas': str.split('M H ~'),
            'consonants': str.split("""
                            k K g G f
                            c C j J F
                            t T d D N
                            w W x X n
                            p P b B m
                            y r l v
                            S R s h
                            ḻ kR jF
                            """),
            'symbols': str.split("""
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
    IAST: iast_scheme,
    KOLKATA: IastScheme(kolkata_variant=True),
    SLP1: Slp1Scheme(),
    WX: WxScheme(),
    TITUS: TitusScheme()
}

ALL_SCHEME_IDS = SCHEMES.keys()

