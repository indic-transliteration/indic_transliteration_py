from indic_transliteration.sanscript.schemes.brahmic import BrahmicScheme, s


class GunjalaGondiScheme(BrahmicScheme):
    def __init__(self):
        super(GunjalaGondiScheme, self).__init__({
            'vowels': s("""𑵠 𑵡 𑵢 𑵣 𑵤 𑵥 ఋ ౠ ఌ ౡ 𑵧 𑵨 𑵪 𑵫 ఎ ఒ"""),
            'marks': s("""𑶊 𑶋 𑶌 𑶍 𑶎 ృ ౄ ౢ ౣ 𑶐 𑶑 𑶓 𑶔 ె  ొ"""),
            'virama': s('𑶗'),
            'yogavaahas': s('𑶕 𑶖 ఁ'),
            'consonants': s("""
                            𑵱 𑵲 𑵶 𑵷 𑶄
                            𑵻 𑵼 𑶀 𑶁 ఞ
                            𑵽 𑵾 𑶂 𑶃 𑵿
                            𑵳 𑵴 𑵸 𑵹 𑵺
                            𑶅 𑶆 𑵮 𑵯 𑵰
                            𑵬 𑶈 𑵵 𑵭
                            శ ష 𑶉 𑶇
                            ళ 𑵱𑶗ష 𑶀𑶗ఞ
                            """)
                          + s("""ऩ ఱ ఴ क़ ఖ ग़ ज़ ड़ ఢ ఫ य़"""),
            'symbols': s("""
                       𑶘 ఽ । ॥
                       𑶠 𑶡 𑶢 𑶣 𑶤 𑶥 𑶦 𑶧 𑶨 𑶩
                       """)
        }, name=GUNJALA_GONDI)


GUNJALA_GONDI = 'gunjala_gondi'
SCHEMES = {
    GUNJALA_GONDI: GunjalaGondiScheme()
}
