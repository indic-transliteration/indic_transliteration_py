# Brahmi schemes
# -------------
import sys

from indic_transliteration.sanscript import Scheme

BENGALI = 'bengali'
DEVANAGARI = 'devanagari'
GUJARATI = 'gujarati'
GURMUKHI = 'gurmukhi'
KANNADA = 'kannada'
MALAYALAM = 'malayalam'
ORIYA = 'oriya'
TAMIL = 'tamil'
TELUGU = 'telugu'



s = str.split
if sys.version_info < (3, 0):
    # noinspection PyUnresolvedReferences
    s = unicode.split

class DevanagariScheme(Scheme):
    def __init__(self):
        super(DevanagariScheme, self).__init__({
            'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ ऎ ऒ"""),
            'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ ॆ ॊ"""),
            'virama': s('्'),
            'yogavaahas': s('ं ः ँ'),
            'consonants': s("""
                            क ख ग घ ङ
                            च छ ज झ ञ
                            ट ठ ड ढ ण
                            त थ द ध न
                            प फ ब भ म
                            य र ल व
                            श ष स ह
                            ळ क्ष ज्ञ
                            """) + s("""ऩ ऱ ऴ"""),
            'symbols': s("""
                       ॐ ऽ । ॥
                       ० १ २ ३ ४ ५ ६ ७ ८ ९
                       """)
        }, is_roman=False, name=DEVANAGARI)

    @classmethod
    def fix_lazy_visarga(cls, data_in):
        data_out = data_in
        import regex
        data_out = regex.sub(r'ः( *)([क-ङ])', r'ᳵ\1\2',   data_out)
        data_out = regex.sub(r'ः( *)([प-म])', r'ᳶ\1\2',   data_out)
        return data_out


class GujaratiScheme(Scheme):
    def __init__(self):
        super(GujaratiScheme, self).__init__({
            'vowels': s("""અ આ ઇ ઈ ઉ ઊ ઋ ૠ ઌ ૡ એ ઐ ઓ ઔ"""),
            'marks': s("""ા િ ી ુ ૂ ૃ ૄ ૢ ૣ ે ૈ ો ૌ"""),
            'virama': s('્'),
            'yogavaahas': s('ં ઃ ઁ'),
            'consonants': s("""
                            ક ખ ગ ઘ ઙ
                            ચ છ જ ઝ ઞ
                            ટ ઠ ડ ઢ ણ
                            ત થ દ ધ ન
                            પ ફ બ ભ મ
                            ય ર લ વ
                            શ ષ સ હ
                            ળ ક્ષ જ્ઞ
                            """),
            'symbols': s("""
                       ૐ ઽ ૤ ૥
                       ૦ ૧ ૨ ૩ ૪ ૫ ૬ ૭ ૮ ૯
                       """)
        }, is_roman=False, name=GUJARATI)



class GurmukhiScheme(Scheme):
    def __init__(self):
        super(GurmukhiScheme, self).__init__({
            'vowels': s("""ਅ ਆ ਇ ਈ ਉ ਊ ऋ ॠ ऌ ॡ ਏ ਐ ਓ ਔ"""),
            'marks': ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', '', '',
                      '', '', 'ੇ', 'ੈ', 'ੋ', 'ੌ'],
            'virama': s('੍'),
            'yogavaahas': s('ਂ ਃ ਁ'),
            'consonants': s("""
                            ਕ ਖ ਗ ਘ ਙ
                            ਚ ਛ ਜ ਝ ਞ
                            ਟ ਠ ਡ ਢ ਣ
                            ਤ ਥ ਦ ਧ ਨ
                            ਪ ਫ ਬ ਭ ਮ
                            ਯ ਰ ਲ ਵ
                            ਸ਼ ਸ਼ ਸ ਹ
                            ਲ਼ ਕ੍ਸ਼ ਜ੍ਞ
                            """),
            'symbols': s("""
                       ੴ ऽ । ॥
                       ੦ ੧ ੨ ੩ ੪ ੫ ੬ ੭ ੮ ੯
                       """)
        }, is_roman=False, name=GURMUKHI)



class KannadaScheme(Scheme):
    def __init__(self):
        super(KannadaScheme, self).__init__({
            'vowels': s("""ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ ಎ ಒ"""),
            'marks': s("""ಾ ಿ ೀ ು ೂ ೃ ೄ ೢ ೣ ೇ ೈ ೋ ೌ ೆ ೊ"""),
            'virama': s('್'),
            'yogavaahas': s('ಂ ಃ ँ'),
            'consonants': s("""
                            ಕ ಖ ಗ ಘ ಙ
                            ಚ ಛ ಜ ಝ ಞ
                            ಟ ಠ ಡ ಢ ಣ
                            ತ ಥ ದ ಧ ನ
                            ಪ ಫ ಬ ಭ ಮ
                            ಯ ರ ಲ ವ
                            ಶ ಷ ಸ ಹ
                            ಳ ಕ್ಷ ಜ್ಞ
                            """) + s("""ऩ ಱ ೞ"""),
            'symbols': s("""
                       ಓಂ ऽ । ॥
                       ೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯
                       """)
        }, is_roman=False, name=KANNADA)



class MalayalamScheme(Scheme):
    def __init__(self):
        super(MalayalamScheme, self).__init__({
            'vowels': s("""അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ എ ഓ"""),
            'marks': s("""ാ ി ീ ു ൂ ൃ ൄ ൢ ൣ േ ൈ ോ ൌ െ ൊ"""),
            'virama': s('്'),
            'yogavaahas': s('ം ഃ ँ'),
            'consonants': s("""
                            ക ഖ ഗ ഘ ങ
                            ച ഛ ജ ഝ ഞ
                            ട ഠ ഡ ഢ ണ
                            ത ഥ ദ ധ ന
                            പ ഫ ബ ഭ മ
                            യ ര ല വ
                            ശ ഷ സ ഹ
                            ള ക്ഷ ജ്ഞ
                            """) + s("""ഩ ള ൟ"""),
            'symbols': s("""
                       ഓം ഽ । ॥
                       ൦ ൧ ൨ ൩ ൪ ൫ ൬ ൭ ൮ ൯
                       """)
        }, is_roman=False, name=MALAYALAM)



class OriyaScheme(Scheme):
    def __init__(self):
        super(OriyaScheme, self).__init__({
            'vowels': s("""ଅ ଆ ଇ ଈ ଉ ଊ ଋ ୠ ଌ ୡ ଏ ଐ ଓ ଔ"""),
            'marks': ['ା', 'ି', 'ୀ', 'ୁ', 'ୂ', 'ୃ', 'ୄ',
                      '', '', 'େ', 'ୈ', 'ୋ', 'ୌ'],
            'virama': s('୍'),
            'yogavaahas': s('ଂ ଃ ଁ'),
            'consonants': s("""
                            କ ଖ ଗ ଘ ଙ
                            ଚ ଛ ଜ ଝ ଞ
                            ଟ ଠ ଡ ଢ ଣ
                            ତ ଥ ଦ ଧ ନ
                            ପ ଫ ବ ଭ ମ
                            ଯ ର ଲ ଵ
                            ଶ ଷ ସ ହ
                            ଳ କ୍ଷ ଜ୍ଞ
                            """),
            'symbols': s("""
                       ଓଂ ଽ । ॥
                       ୦ ୧ ୨ ୩ ୪ ୫ ୬ ୭ ୮ ୯
                       """)
        }, is_roman=False, name=ORIYA)



class TamilScheme(Scheme):
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
        }, is_roman=False, name=TAMIL)


class TeluguScheme(Scheme):
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
                            """),
            'symbols': s("""
                       ఓం ఽ । ॥
                       ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯
                       """)
        }, is_roman=False, name=TELUGU)


class BengaliScheme(Scheme):
    def __init__(self):
        super(BengaliScheme, self).__init__({
            'vowels': s("""অ আ ই ঈ উ ঊ ঋ ৠ ঌ ৡ এ ঐ ও ঔ"""),
            'marks': s("""া ি ী ু ূ ৃ ৄ ৢ ৣ ে ৈ ো ৌ"""),
            'virama': s('্'),
            'yogavaahas': s('ং ঃ ঁ'),
            'consonants': s("""
                            ক খ গ ঘ ঙ
                            চ ছ জ ঝ ঞ
                            ট ঠ ড ঢ ণ
                            ত থ দ ধ ন
                            প ফ ব ভ ম
                            য র ল ব
                            শ ষ স হ
                            ळ ক্ষ জ্ঞ
                            """),
            'symbols': s("""
                       ॐ ঽ । ॥
                       ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯
                       """)
        }, is_roman=False, name=BENGALI)
