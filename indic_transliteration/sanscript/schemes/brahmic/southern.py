from indic_transliteration.sanscript.schemes.brahmic import BrahmicScheme


class KannadaScheme(BrahmicScheme):
    def __init__(self):
        super(KannadaScheme, self).__init__({
            'vowels': str.split("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ ಎ ಒ"""),
            'marks': str.split("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೇ ೈ ೋ ೌ ೆ ೊ"""),
            'virama': str.split('್'),
            'yogavaahas': str.split('ಂ ಃ ಁ ೱ ೲ ಼'),
            'consonants': str.split("""
                            ಕ ಖ ಗ ಘ ಙ
                            ಚ ಛ ಜ ಝ ಞ
                            ಟ ಠ ಡ ಢ ಣ
                            ತ ಥ ದ ಧ ನ
                            ಪ ಫ ಬ ಭ ಮ
                            ಯ ರ ಲ ವ
                            ಶ ಷ ಸ ಹ
                            ಳ ಕ್ಷ ಜ್ಞ
                            """)
                          + str.split("""ನ಼ ಱ ೞ ಕ಼ ಖ಼ ಗ಼ ಜ಼ ಡ಼ ಢ಼ ಫ಼ ಯ಼"""),
            'symbols': str.split("""
                       ಓಂ ಽ । ॥
                       ೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯
                       """)
        }, name=KANNADA)


class MalayalamScheme(BrahmicScheme):
    def __init__(self):
        super(MalayalamScheme, self).__init__({
            'vowels': str.split("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ എ ഒ"""),
            'marks': str.split("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ േ ൈ ോ ൌ െ ൊ"""),
            'virama': str.split('്'),
            'yogavaahas': str.split('ം ഃ ഁ'),
            'consonants': str.split("""
                            ക ഖ ഗ ഘ ങ
                            ച ഛ ജ ഝ ഞ
                            ട ഠ ഡ ഢ ണ
                            ത ഥ ദ ധ ന
                            പ ഫ ബ ഭ മ
                            യ ര ല വ
                            ശ ഷ സ ഹ
                            ള ക്ഷ ജ്ഞ
                            """) + str.split("""ഩ റ ഴ"""),
            'symbols': str.split("""
                       ഓം ഽ । ॥
                       ൦ ൧ ൨ ൩ ൪ ൫ ൬ ൭ ൮ ൯
                       """)
        }, name=MALAYALAM)


class TamilScheme(BrahmicScheme):
    def __init__(self):
        super(TamilScheme, self).__init__({
            'vowels': str.split("""அ ஆ இ ஈ உ ஊ ரு ரூ லு லூ ஏ ஐ ஓ ஔ எ ஒ"""),
            'marks': ['ா', 'ி', 'ீ', 'ு', 'ூ', '்ரு', '்ரூ',
                      '்லு', '்லூ', 'ே', 'ை', 'ோ', 'ௌ'] + ['ெ', 'ொ'],
            'virama': str.split('்'),
            'yogavaahas': str.split('ம் ஃ ँ'),
            'consonants': str.split("""
                            க க க க ங
                            ச ச ஜ ச ஞ
                            ட ட ட ட ண
                            த த த த ந
                            ப ப ப ப ம
                            ய ர ல வ
                            ஶ ஷ ஸ ஹ
                            ள க்ஷ ஜ்ஞ
                            """) + str.split("""ன ற ழ"""),
            'symbols': str.split("""
                       ௐ ऽ । ॥
                       ௦ ௧ ௨ ௩ ௪ ௫ ௬ ௭ ௮ ௯
                       """)
        }, name=TAMIL)


class GranthaScheme(BrahmicScheme):
    def __init__(self):
        super(GranthaScheme, self).__init__({
            'vowels': str.split("""𑌅 𑌆 𑌇 𑌈 𑌉 𑌊 𑌋 𑍠 𑌌 𑍡 𑌏 𑌐 𑌓 𑌔 𑌏𑌀 𑌓𑌀"""),
            'marks': str.split("""𑌾 𑌿 𑍀 𑍁 𑍂 𑍃 𑍄 𑍢 𑍣 𑍇 𑍈 𑍋 𑍗 𑍇𑌀 𑍋𑌀"""),
            'virama': str.split('𑍍'),
            'yogavaahas': str.split('𑌂 𑌃 𑌁'),
            'consonants': str.split("""
                            𑌕 𑌖 𑌗 𑌘 𑌙
                            𑌚 𑌛 𑌜 𑌝 𑌞
                            𑌟 𑌠 𑌡 𑌢 𑌣
                            𑌤 𑌥 𑌦 𑌧 𑌨
                            𑌪 𑌫 𑌬 𑌭 𑌮
                            𑌯 𑌰 𑌲 𑌵
                            𑌳 𑌕𑍍𑌷 𑌜𑍍𑌞
                            𑌨𑌼 𑌰𑌼 𑌳𑌼
                            """) + str.split("""ன ற ழ"""),
            'symbols': str.split("""
                       𑍐 𑌽 । ॥
                       ௦ ௧ ௨ ௩ ௪ ௫ ௬ ௭ ௮ ௯
                       """)
        }, name=GRANTHA)


class TeluguScheme(BrahmicScheme):
    def __init__(self):
        super(TeluguScheme, self).__init__({
            'vowels': str.split("""అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ ఎ ఒ"""),
            'marks': str.split("""ా ి ీ ు ూ ృ ౄ ౢ ౣ ే ై ో ౌ ె  ొ"""),
            'virama': str.split('్'),
            'yogavaahas': str.split('ం ః ఁ'),
            'consonants': str.split("""
                            క ఖ గ ఘ ఙ
                            చ ఛ జ ఝ ఞ
                            ట ఠ డ ఢ ణ
                            త థ ద ధ న
                            ప ఫ బ భ మ
                            య ర ల వ
                            శ ష స హ
                            ళ క్ష జ్ఞ
                            """)
                          + str.split("""ऩ ఱ ఴ क़ ఖ ग़ ज़ ड़ ఢ ఫ य़"""),
            'symbols': str.split("""
                       ఓం ఽ । ॥
                       ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯
                       """)
        }, name=TELUGU)


KANNADA = 'kannada'
MALAYALAM = 'malayalam'
TAMIL = 'tamil'
GRANTHA = 'grantha'
TELUGU = 'telugu'
SCHEMES = {
    KANNADA: KannadaScheme(),
    MALAYALAM: MalayalamScheme(),
    TAMIL: TamilScheme(),
    GRANTHA: GranthaScheme(),
    TELUGU: TeluguScheme()
}
