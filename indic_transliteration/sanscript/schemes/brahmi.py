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
            'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ"""),
            'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ"""),
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
                            """),
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
