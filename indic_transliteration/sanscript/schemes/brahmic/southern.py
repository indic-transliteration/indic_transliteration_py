from indic_transliteration.sanscript.schemes.brahmic import BrahmicScheme, s


class KannadaScheme(BrahmicScheme):
    def __init__(self):
        super(KannadaScheme, self).__init__({
            'vowels': s("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ ಎ ಒ"""),
            'marks': s("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೇ ೈ ೋ ೌ ೆ ೊ"""),
            'virama': s('್'),
            'yogavaahas': s('ಂ ಃ ಁ ೱ ೲ ಼'),
            'consonants': s("""
                            ಕ ಖ ಗ ಘ ಙ
                            ಚ ಛ ಜ ಝ ಞ
                            ಟ ಠ ಡ ಢ ಣ
                            ತ ಥ ದ ಧ ನ
                            ಪ ಫ ಬ ಭ ಮ
                            ಯ ರ ಲ ವ
                            ಶ ಷ ಸ ಹ
                            ಳ ಕ್ಷ ಜ್ಞ
                            """)
                          + s("""ನ಼ ಱ ೞ ಕ಼ ಖ಼ ಗ಼ ಜ಼ ಡ಼ ಢ಼ ಫ಼ ಯ಼"""),
            'symbols': s("""
                       ಓಂ ಽ । ॥
                       ೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯
                       """)
        }, name=KANNADA)


class MalayalamScheme(BrahmicScheme):
    def __init__(self):
        super(MalayalamScheme, self).__init__({
            'vowels': s("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ എ ഒ"""),
            'marks': s("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ േ ൈ ോ ൌ െ ൊ"""),
            'virama': s('്'),
            'yogavaahas': s('ം ഃ ഁ'),
            'consonants': s("""
                            ക ഖ ഗ ഘ ങ
                            ച ഛ ജ ഝ ഞ
                            ട ഠ ഡ ഢ ണ
                            ത ഥ ദ ധ ന
                            പ ഫ ബ ഭ മ
                            യ ര ല വ
                            ശ ഷ സ ഹ
                            ള ക്ഷ ജ്ഞ
                            """) + s("""ഩ റ ഴ"""),
            'symbols': s("""
                       ഓം ഽ । ॥
                       ൦ ൧ ൨ ൩ ൪ ൫ ൬ ൭ ൮ ൯
                       """)
        }, name=MALAYALAM)


class TamilScheme(BrahmicScheme):
    def __init__(self):
        super(TamilScheme, self).__init__({
            'vowels': s("""அ ஆ இ ஈ உ ஊ ऋ ॠ ऌ ॡ ஏ ஐ ஓ ஔ எ ஒ"""),
            'marks': ['ா', 'ி', 'ீ', 'ு', 'ூ', '', '',
                      '', '', 'ே', 'ை', 'ோ', 'ௌ'] + ['ெ', 'ொ'],
            'virama': s('்'),
            'yogavaahas': s('ஂ ஃ ँ'),
            'consonants': s("""
                            க க க க ங
                            ச ச ஜ ச ஞ
                            ட ட ட ட ண
                            த த த த ந
                            ப ப ப ப ம
                            ய ர ல வ
                            ஶ ஷ ஸ ஹ
                            ள க்ஷ ஜ்ஞ
                            """) + s("""ன ற ழ"""),
            'symbols': s("""
                       ௐ ऽ । ॥
                       ௦ ௧ ௨ ௩ ௪ ௫ ௬ ௭ ௮ ௯
                       """)
        }, name=TAMIL)


class TeluguScheme(BrahmicScheme):
    def __init__(self):
        super(TeluguScheme, self).__init__({
            'vowels': s("""అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ ఎ ఒ"""),
            'marks': s("""ా ి ీ ు ూ ృ ౄ ౢ ౣ ే ై ో ౌ ె  ొ"""),
            'virama': s('్'),
            'yogavaahas': s('ం ః ఁ'),
            'consonants': s("""
                            క ఖ గ ఘ ఙ
                            చ ఛ జ ఝ ఞ
                            ట ఠ డ ఢ ణ
                            త థ ద ధ న
                            ప ఫ బ భ మ
                            య ర ల వ
                            శ ష స హ
                            ళ క్ష జ్ఞ
                            """)
                          + s("""ऩ ऱ ऴ क़ ఖ ग़ ज़ ड़ ఢ ఫ य़"""),
            'symbols': s("""
                       ఓం ఽ । ॥
                       ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯
                       """)
        }, name=TELUGU)


KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TAMIL = 'tamil'
TELUGU = 'telugu'
SCHEMES = {
    KANNADA: KannadaScheme(),
    MALAYALAM: MalayalamScheme(),
    TAMIL: TamilScheme(),
    TELUGU: TeluguScheme()
}
