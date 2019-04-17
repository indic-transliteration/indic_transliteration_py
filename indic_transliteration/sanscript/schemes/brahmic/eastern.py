from indic_transliteration.sanscript.schemes.brahmic import BrahmicScheme, s


class BengaliScheme(BrahmicScheme):
    def __init__(self):
        super(BengaliScheme, self).__init__({
            'vowels': s("""অ আ ই ঈ উ ঊ ঋ ৠ ঌ ৡ এ ঐ ও ঔ"""),
            'marks': s("""া ি ী ু ূ ৃ ৄ ৢ ৣ ে ৈ ো ৌ"""),
            'virama': s('্'),
            'yogavaahas': s('ং ঃ ঁ ᳵ ᳶ ়'),
            'consonants': s("""
                            ক খ গ ঘ ঙ
                            চ ছ জ ঝ ঞ
                            ট ঠ ড ঢ ণ
                            ত থ দ ধ ন
                            প ফ ব ভ ম
                            য র ল ব
                            শ ষ স হ
                            ळ ক্ষ জ্ঞ
                            """)
                          + s("""ন় র় ষ় ক় খ় গ় জ় ড় ঢ় ফ় য়"""),
            'symbols': s("""
                       ॐ ঽ । ॥
                       ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯
                       """)
        }, name=BENGALI)


class OriyaScheme(BrahmicScheme):
    def __init__(self):
        super(OriyaScheme, self).__init__({
            'vowels': s("""ଅ ଆ ଇ ଈ ଉ ଊ ଋ ୠ ଌ ୡ ଏ ଐ ଓ ଔ"""),
            'marks': ['ା', 'ି', 'ୀ', 'ୁ', 'ୂ', 'ୃ', 'ୄ',
                      '', '', 'େ', 'ୈ', 'ୋ', 'ୌ'],
            'virama': s('୍'),
            'yogavaahas': s('ଂ ଃ ଁ ᳵ ᳶ ଼'),
            'consonants': s("""
                            କ ଖ ଗ ଘ ଙ
                            ଚ ଛ ଜ ଝ ଞ
                            ଟ ଠ ଡ ଢ ଣ
                            ତ ଥ ଦ ଧ ନ
                            ପ ଫ ବ ଭ ମ
                            ଯ ର ଲ ଵ
                            ଶ ଷ ସ ହ
                            ଳ କ୍ଷ ଜ୍ଞ
                            """)
                          + s("""ନ଼ ର଼ ଳ଼ କ଼ ଖ଼ ଗ଼ ଜ଼ ଡ଼ ଢ଼ ଫ଼ ୟ"""),
            'symbols': s("""
                       ଓଂ ଽ । ॥
                       ୦ ୧ ୨ ୩ ୪ ୫ ୬ ୭ ୮ ୯
                       """)
        }, name=ORIYA)


BENGALI = 'bengali'
ORIYA = 'oriya'
SCHEMES = {
    BENGALI: BengaliScheme(),
    ORIYA: OriyaScheme(),
}
