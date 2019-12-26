from indic_transliteration.sanscript.schemes.brahmic import BrahmicScheme, s


class DevanagariScheme(BrahmicScheme):
    def __init__(self):
        super(DevanagariScheme, self).__init__({
            'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ ऎ ऒ"""),
            'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ ॆ ॊ"""),
            'virama': s('्'),
            'yogavaahas': s('ं ः ँ ᳵ ᳶ ़'),
            'consonants': s("""
                            क ख ग घ ङ
                            च छ ज झ ञ
                            ट ठ ड ढ ण
                            त थ द ध न
                            प फ ब भ म
                            य र ल व
                            श ष स ह
                            ळ क्ष ज्ञ
                            """)
                          + s("""ऩ ऱ ऴ क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़"""),
            'symbols': s("""
                       ॐ ऽ । ॥
                       ० १ २ ३ ४ ५ ६ ७ ८ ९
                       """)
        }, name=DEVANAGARI, synonym_map={'फ़': ["फ़"], "ड़": ["ड़"]})

    @classmethod
    def fix_lazy_visarga(cls, data_in):
        data_out = data_in
        import regex
        data_out = regex.sub(r'ः( *)([क-ङ])', r'ᳵ\1\2',   data_out)
        data_out = regex.sub(r'ः( *)([प-म])', r'ᳶ\1\2',   data_out)
        return data_out


class GujaratiScheme(BrahmicScheme):
    def __init__(self):
        super(GujaratiScheme, self).__init__({
            'vowels': s("""અ આ ઇ ઈ ઉ ઊ ઋ ૠ ઌ ૡ એ ઐ ઓ ઔ"""),
            'marks': s("""ા િ ી ુ ૂ ૃ ૄ ૢ ૣ ે ૈ ો ૌ"""),
            'virama': s('્'),
            'yogavaahas': s('ં ઃ ઁ ᳵ ᳶ ઼'),
            'consonants': s("""
                            ક ખ ગ ઘ ઙ
                            ચ છ જ ઝ ઞ
                            ટ ઠ ડ ઢ ણ
                            ત થ દ ધ ન
                            પ ફ બ ભ મ
                            ય ર લ વ
                            શ ષ સ હ
                            ળ ક્ષ જ્ઞ
                            """)
                          + s("""ન઼ ર઼ ળ઼ ક઼ ખ઼ ગ઼ જ઼ ડ઼ ઢ઼ ફ઼ ય઼"""),
            'symbols': s("""
                       ૐ ઽ । ॥
                       ૦ ૧ ૨ ૩ ૪ ૫ ૬ ૭ ૮ ૯
                       """)
        }, name=GUJARATI)


class GurmukhiScheme(BrahmicScheme):
    def __init__(self):
        super(GurmukhiScheme, self).__init__({
            'vowels': s("""ਅ ਆ ਇ ਈ ਉ ਊ ऋ ॠ ऌ ॡ ਏ ਐ ਓ ਔ"""),
            'marks': ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', 'ृ', 'ॄ',
                      'ॢ', 'ॣ', 'ੇ', 'ੈ', 'ੋ', 'ੌ'], # Includes some fake mAtrA-s from devanAgarI
            'virama': s('੍'),
            'yogavaahas': s('ਂ ਃ ਁ ᳵ ᳶ ਼'),
            'consonants': s("""
                            ਕ ਖ ਗ ਘ ਙ
                            ਚ ਛ ਜ ਝ ਞ
                            ਟ ਠ ਡ ਢ ਣ
                            ਤ ਥ ਦ ਧ ਨ
                            ਪ ਫ ਬ ਭ ਮ
                            ਯ ਰ ਲ ਵ
                            ਸ਼ ਸ਼਼ ਸ ਹ
                            ਲ਼ ਕ੍ਸ਼ ਜ੍ਞ
                            """)
                          + s("""ਨ਼ ਰ਼ ਲ਼਼ ਕ਼ ਖ਼ ਗ਼ ਜ਼ ੜ ਢ਼ ਫ਼ ਯ਼"""),
            'symbols': s("""
                       ੴ ऽ । ॥
                       ੦ ੧ ੨ ੩ ੪ ੫ ੬ ੭ ੮ ੯
                       """)
        }, name=GURMUKHI, synonym_map={"ਂ": ["ੰ"]})

    @classmethod
    def replace_tippi(cls, text):
        import regex
        text = regex.sub("ੱ([ਕਖ])", r"ਕ੍\g<1>", text, flags=regex.UNICODE)
        text = regex.sub(r"ੱ([ਗਘ])", "ਗ੍\g<1>", text)
        text = regex.sub("ੱ([ਚਛ])", "ਚ੍\g<1>", text)
        text = regex.sub("ੱ([ਜਝ])", "ਜ੍\g<1>", text)
        text = regex.sub("ੱ([ਟਠ])", "ਟ੍\g<1>", text)
        text = regex.sub("ੱ([ਡਢ])", "ਡ੍\g<1>", text)
        text = regex.sub("ੱ([ਤਥ])", "ਤ੍\g<1>", text)
        text = regex.sub("ੱ([ਦਧ])", "ਦ੍\g<1>", text)
        text = regex.sub("ੱ([ਪਫ])", "ਪ੍\g<1>", text)
        text = regex.sub("ੱ([ਬਭ])", "ਬ੍\g<1>", text)
        text = regex.sub("ੱ([ਯਰਲਵਸ਼ਸਹਙਞਣਨਮਜ਼ੜਫ਼])", "\g<1>੍\g<1>", text)
        return text


DEVANAGARI = 'devanagari'
GUJARATI = 'gujarati'
GURMUKHI = 'gurmukhi'
SCHEMES = {
    DEVANAGARI: DevanagariScheme(),
    GUJARATI: GujaratiScheme(),
    GURMUKHI: GurmukhiScheme(),
}
