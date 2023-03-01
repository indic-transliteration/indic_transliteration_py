from indic_transliteration.sanscript.schemes.brahmic import accent
from indic_transliteration import sanscript


def test_move_accent_to_previous_syllable():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="सैॗषा᳘ निदा᳘नेना यदि᳘डा॥", old_accent="ॗ", new_accent="ॗ") == "ॗसैषा᳘ निदा᳘नेना यदि᳘डा॥"
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।", old_accent="᳕", new_accent="ॗ") == "तॖस्माद्वाॖ अप॑ उॖपस्पृशतिॗ॥ सोऽग्निॖमेॗवाभीॖक्षमाणः।".replace("ॖ", "॑")


def test_set_diirgha_svaritas():
  assert accent.set_diirgha_svaritas(scheme=sanscript.SCHEMES[sanscript.DEVANAGARI], text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।") == "त॑स्माद्वा᳚ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी᳚क्षमाणः।"