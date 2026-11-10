from indic_transliteration.sanscript.schemes.brahmic import accent
from indic_transliteration import sanscript


def test_move_accent_to_previous_syllable():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="सैॗषा᳘ निदा᳘नेना यदि᳘डा॥", old_accent="ॗ", new_accent="ॗ") == "ॗसैषा᳘ निदा᳘नेना यदि᳘डा॥"
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।", old_accent="᳕", new_accent="ॗ") == "तॖस्माद्वाॖ अप॑ उॖपस्पृशतिॗ॥ सोऽग्निॖमेॗवाभीॖक्षमाणः।".replace("ॖ", "॑")


def test_set_diirgha_svaritas():
  assert accent.set_diirgha_svaritas(scheme=sanscript.SCHEMES[sanscript.DEVANAGARI], text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।") == "त॑स्माद्वा᳚ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी᳚क्षमाणः।"
  
  
def test_to_US_accents():
  assert accent.to_US_accents(text="ग्रहो॑ भवति दर्शपूर्णमा॒सयो॑स्सृ॒ष्टयो॒र्धृत्यै॑  ।    \n\nसो॑ऽकामयत चातुर्मा॒स्यानि॑ सृजे॒येति॑ ।") == "ग्र᳓हो भवति दर्शपूर्णमास᳓योस्सृष्ट᳓योर्धृ᳓त्यै  ।    \n\nसो᳓ऽकामयत चातुर्मास्या᳓नि सृजेये᳓ति ।"
  assert accent.to_US_accents(text="न्यू॑नया जुहोति") == "न्यू᳙नया जुहोति"
  assert accent.to_US_accents(text="स मे॑ ददातु प्र॒जां प॒शून् पुष्टिय्ँ॒ यशः॑") == "स᳓ मे ददातु प्रजां᳓ पशू᳓न् पु᳓ष्टिय्ँ य᳓शः"
  assert accent.to_US_accents(text="सो॑ ऽनाधृ॒ष्यः ।(9)") == "सो᳓ ऽनाधृष्यः᳓ ।(9)"
  assert accent.to_US_accents(text="""ध्रु॒वो॑ऽसि ।  \nध्रु॒वो॒॑ऽहँ स॑जा॒तेषु॑+++(=haya)+++ भूयास॒न्  \nधीर॒श् चेत्ता॑ वसु॒वित्।""", SVARITA_NEW="᳕", UDATTA="꣡") == "ध्रुवो᳕ऽसि ।  \nध्रुवो꣡ऽहँ꣡ सजाते꣡षु+++(=haya)+++ भूयासन्  \nधी꣡रश् चे꣡त्ता वसुवि꣡त्।"
  assert accent.to_US_accents(text="\"यज॑मानेन॒ खलु॒ वै तत् का॒र्य॑म्\" इत्य् आ॑हु॒र्", SVARITA_NEW="᳕", UDATTA="꣡") == "\"य꣡जमानेन ख꣡लु वै꣡ त꣡त् कार्य᳕म्\" इ꣡त्य् आहुर्"
  
  assert accent.to_US_accents(text="\"स त्वा+++(←तु + वै)+++ इडा॒म् उप॑ह्वयेत॒,", SVARITA_NEW="᳕", UDATTA="꣡") == "\"स꣡ त्वा꣡+++(←तु + वै)+++ इ꣡डाम् उ꣡पह्वयेत,"
  assert accent.to_US_accents(text="ए॒तत्प्रति॒ वा असु॑राणाय्ँ य॒ज्ञो व्य॑च्छिद्यत ।  ", SVARITA_NEW="᳕", UDATTA="꣡") == "एत꣡त्प्र꣡ति वा꣡ अ꣡सुराणाय्ँ यज्ञो꣡ व्यच्छिद्यत ।  "


def test_add_dependent_accents():
  # A dependent svarita gets DEP_SVARITA, and an anudAtta rising to an accent gets a sannatara.
  # UDATTA_NEW defaults to UDATTA, so udAtta marks are retained.
  assert accent.add_dependent_accents(text="ग्र᳓हो भवति दर्शपूर्णमास᳓योस्सृष्ट᳓योर्धृ᳓त्यै  ।") == "ग्र᳓हो᳜ भवति दर्शपूर्णमा॒स᳓यो᳜स्सृ॒ष्ट᳓यो॒र्धृ᳓त्यै᳜  ।"
  # Pass DEP_SVARITA="॑" to get classical Yajurveda print style, and UDATTA_NEW="" to leave udAttas unmarked.
  assert accent.add_dependent_accents(text="ग्र᳓हो भवति दर्शपूर्णमास᳓योस्सृष्ट᳓योर्धृ᳓त्यै  ।", DEP_SVARITA="॑", UDATTA_NEW="") == "ग्रहो॑ भवति दर्शपूर्णमा॒सयो॑स्सृ॒ष्टयो॒र्धृत्यै॑  ।"
  # Independent svaritas (᳙) are left untouched.
  assert accent.add_dependent_accents(text="न्यू᳙नया जुहोति") == "न्यू᳙नया जुहोति"
  # An udAtta followed by another udAtta does not produce a svarita.
  assert accent.add_dependent_accents(text="ध्रुवो꣡ऽहँ꣡ सजाते꣡षु+++(=haya)+++ भूयासन्", UDATTA="꣡", DEP_SVARITA="॑", UDATTA_NEW="") == "ध्रु॒वोऽहँ स॑जा॒तेषु॑+++(=haya)+++ भूयासन्"
  # Text already containing dependent accents is not accented twice.
  assert accent.add_dependent_accents(text="ग्रहो᳜ भवति") == "ग्रहो᳜ भवति"


def test_add_dependent_accents_round_trip():
  # Note: to_US_accents loses some accent information (e.g. some independent svaritas at the start of a phrase).
  for text in ["स मे॑ ददातु प्र॒जां प॒शून् पुष्टिय्ँ॒ यशः॑",
               "दर्शपूर्णमा॒सयो॑स्सृ॒ष्टयो॒र्धृत्यै॑  ।",
               "चातुर्मा॒स्यानि॑ सृजे॒येति॑ ।",
               "ए॒तत्प्रति॒ वा असु॑राणाय्ँ य॒ज्ञो व्य॑च्छिद्यत ।  "]:
    assert accent.add_dependent_accents(text=accent.to_US_accents(text=text), DEP_SVARITA="॑", UDATTA_NEW="") == text
