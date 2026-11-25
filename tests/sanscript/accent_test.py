from indic_transliteration.sanscript.schemes.brahmic import accent
from indic_transliteration import sanscript


def test_move_accent_to_previous_syllable():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="सैॗषा᳘ निदा᳘नेना यदि᳘डा॥", old_accent="ॗ", new_accent="ॗ") == "ॗसैषा᳘ निदा᳘नेना यदि᳘डा॥"
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।", old_accent="᳕", new_accent="ॗ") == "तॖस्माद्वाॖ अप॑ उॖपस्पृशतिॗ॥ सोऽग्निॖमेॗवाभीॖक्षमाणः।".replace("ॖ", "॑")


def test_set_diirgha_svaritas():
  assert accent.set_diirgha_svaritas(scheme=sanscript.SCHEMES[sanscript.DEVANAGARI], text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।") == "त॑स्माद्वा᳚ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी᳚क्षमाणः।"
  
  
def test_to_US_accents():
  assert accent.to_US_accents(text="ग्रहो॑ भवति दर्शपूर्णमा॒सयो॑स्सृ॒ष्टयो॒र्धृत्यै॑  ।    \n\nसो॑ऽकामयत चातुर्मा॒स्यानि॑ सृजे॒येति॑ ।") == "ग्र᳓हो भवति दर्शपूर्णमास᳓योस्सृष्ट᳓योर्धृ᳓त्यै  ।    \n\nसो᳙ऽकामयत चातुर्मास्या᳓नि सृजेये᳓ति ।"
  assert accent.to_US_accents(text="न्यू॑नया जुहोति") == "न्यू᳙नया जुहोति"
  assert accent.to_US_accents(text="स्वा॑ग्रयणो॒ जिन्व॑") == "स्वा᳙ग्रयणो जि᳓न्व"
  assert accent.to_US_accents(text="ध्रु॒वो॑ न्यू॑नया जुहोति") == "ध्रुवो᳙ न्यू᳙नया जुहोति"
  assert accent.to_US_accents(text="स मे॑ ददातु प्र॒जां प॒शून् पुष्टिय्ँ॒ यशः॑") == "स᳓ मे ददातु प्रजां᳓ पशू᳓न् पु᳓ष्टिय्ँ य᳓शः"
  assert accent.to_US_accents(text="ते नो॑ऽवन्तु") == "ते᳓ नोऽवन्तु"
  assert accent.to_US_accents(text="ए॒व सो॑ऽब्रवीत्") == "एव᳓ सो᳙ऽब्रवीत्"
  assert accent.to_US_accents(text="सो॑ ऽनाधृ॒ष्यः ।(9)") == "सो᳙ ऽनाधृष्यः᳓ ।(9)"
  assert accent.to_US_accents(text="""ध्रु॒वो॑ऽसि ।  \nध्रु॒वो॒॑ऽहँ स॑जा॒तेषु॑+++(=haya)+++ भूयास॒न्  \nधीर॒श् चेत्ता॑ वसु॒वित्।""", SVARITA_NEW="᳕", UDATTA="꣡") == "ध्रुवो᳕ऽसि ।  \nध्रुवो꣡ऽहँ꣡ सजाते꣡षु+++(=haya)+++ भूयासन्  \nधी꣡रश् चे꣡त्ता वसुवि꣡त्।"
  assert accent.to_US_accents(text="\"यज॑मानेन॒ खलु॒ वै तत् का॒र्य॑म्\" इत्य् आ॑हु॒र्", SVARITA_NEW="᳕", UDATTA="꣡") == "\"य꣡जमानेन ख꣡लु वै꣡ त꣡त् कार्य᳕म्\" इ꣡त्य् आहुर्"
  
  assert accent.to_US_accents(text="\"स त्वा+++(←तु + वै)+++ इडा॒म् उप॑ह्वयेत॒,", SVARITA_NEW="᳕", UDATTA="꣡") == "\"स꣡ त्वा꣡+++(←तु + वै)+++ इ꣡डाम् उ꣡पह्वयेत,"
  assert accent.to_US_accents(text="ए॒तत्प्रति॒ वा असु॑राणाय्ँ य॒ज्ञो व्य॑च्छिद्यत ।  ", SVARITA_NEW="᳕", UDATTA="꣡") == "एत꣡त्प्र꣡ति वा꣡ अ꣡सुराणाय्ँ यज्ञो꣡ व्यच्छिद्यत ।  "
  assert accent.to_US_accents(text="यो॑ऽपां पुष्पव्ँ॒ वेद॑") == "यो᳙ऽपां᳓ पु᳓ष्पव्ँ वे᳓द"
  assert accent.to_US_accents(text="यो॑ऽप्सु नावं॒ प्रति॑ष्ठिताव्ँ॒ वेद॑") == "यो᳙ऽप्सु᳓ ना᳓वं प्र᳓तिष्ठिताव्ँ वे᳓द"
  assert accent.to_US_accents(text="यो॑ऽमुष्य॒ तप॑त आ॒यत॑नव्ँ॒ वेद॑") == "यो᳙ऽमु᳓ष्य त᳓पत आय᳓तनव्ँ वे᳓द"
  assert accent.to_US_accents(text="यो॑ ऽपां आ॒यत॑नव्ँ॒ वेद॑") == "यो᳙ ऽपां᳓ आय᳓तनव्ँ वे᳓द"
  assert accent.to_US_accents(text="ये॑ऽर्द्धमा॒साश्च॒ मासा॑श्च॒ ते चा॑तुर्मा॒स्यानि॑") == "ये᳙ऽर्द्धमासा᳓श्च मा᳓साश्च ते᳓ चातुर्मास्या᳓नि"
  assert accent.to_US_accents(text="यो॑ऽस्मान्द्वेष्टि॒ यञ्च॑ व॒यन्द्वि॒ष्मः") == "यो᳙ऽस्मा᳓न्द्वे᳓ष्टि य᳓ञ्च वय᳓न्द्विष्मः᳓"
  assert accent.to_US_accents(text="ये॑ऽस्मिल्ँ लो॒के") == "ये᳙ऽस्मिल्ँ᳓ लोके᳓"
  assert accent.to_US_accents(text="तस्मि॑न्हीयताय्ँ॒ यो॑ऽस्मान् द्वेष्टि॒") == "त᳓स्मिन्हीयताय्ँ यो᳙ऽस्मा᳓न् द्वे᳓ष्टि"
  assert accent.to_US_accents(text="दु॒र्मि॒त्रास्तस्मै॑ भूयासु॒र्यो॑ऽस्मान्द्वेष्टि॒ यञ्च॑ व॒यन्द्वि॒ष्मः") == "दुर्मित्रा᳓स्त᳓स्मै भूयासुर्यो᳙ऽस्मा᳓न्द्वे᳓ष्टि य᳓ञ्च वय᳓न्द्विष्मः᳓"
  assert accent.to_US_accents(text="स भू॑या॒द्यो॑ऽस्मान्द्वेष्टि॒ यञ्च॑ व॒यन्द्वि॒ष्मः") == "स᳓ भूयाद्यो᳙ऽस्मा᳓न्द्वे᳓ष्टि य᳓ञ्च वय᳓न्द्विष्मः᳓"
  assert accent.to_US_accents(text="व्य॑सौ यो॑ऽस्मान्द्वेष्टि॒ यञ्च॑ व॒यन्द्वि॒ष्म इत्या॑ह") == "व्य᳙सौ᳓ यो᳙ऽस्मा᳓न्द्वे᳓ष्टि य᳓ञ्च वय᳓न्द्विष्म᳓ इ᳓त्याह"
  assert accent.to_US_accents(text="अ॒सौ यो॑ऽस्त॒मेति॑") == "असौ᳓ यो᳙ऽस्तमे᳓ति"
  assert accent.to_US_accents(text="ये॑ऽस्मिल्ँलो॒के") == "ये᳙ऽस्मिल्ँ᳓लोके᳓"
  assert accent.to_US_accents(text="माऽऽचा॒र्यो॑ऽब्रवी॒दिति॑ होवाच") == "मा᳓ऽऽचार्यो᳙ऽब्रवीदि᳓ति होवाच"
  assert accent.to_US_accents(text="परि॒षद्यो॑ऽसि॒ पव॑मानः") == "प᳓रिष᳓द्योऽसि प᳓वमानः"
  assert accent.to_US_accents(text="यद्ब्रू॒याद्यो॑ऽग्निँ होता॑र॒मवृ॑था॒ इति॑") == "य᳓द्ब्रूया᳓द्यो᳙ऽग्निँ᳓ हो᳓तारम᳓वृथा इ᳓ति"
  assert accent.to_US_accents(text="अथ॒ ये॑ऽमुतो॒ऽर्वाञ्च॑मुप॒यन्ति॑") == "अ᳓थ ये᳙ऽमु᳓तोऽर्वा᳓ञ्चमुपय᳓न्ति"
  # अरण्येऽनुवाक्यः is an aluk-samāsa (Pāṇini 6.3.9), so अ- is anudātta and यो᳙ is abhinihita svarita.
  assert accent.to_US_accents(text="यो॑ऽरण्येऽनुवा॒क्यो॑ ग॒णः") == "यो᳙ऽरण्येऽनुवाक्यो᳙ गणः᳓"
  assert accent.to_US_accents(text="यो॑ऽग्नेर्दे॒वता॑या॒ एति॑") == "यो᳙ऽग्ने᳓र्देव᳓ताया ए᳓ति"
  assert accent.to_US_accents(text="यो॑ऽस्य प्र॒जाया॒मृध्या॑ता") == "यो᳙ऽस्य प्रजा᳓यामृ᳓ध्याता"
  assert accent.to_US_accents(text="यो॑ऽस्य सोमपी॒थो भ॑वति") == "यो᳙ऽस्य सोमपीथो᳓ भवति"
  assert accent.to_US_accents(text="यो॑ऽस्मै प्र॒जाम्प॒शून्") == "यो᳙ऽस्मै प्रजा᳓म्पशू᳓न्"
  assert accent.to_US_accents(text="सो॒॑ऽग्नये॑ऽध्रियत") == "सो᳓ऽग्न᳓येऽध्रियत"
  assert accent.to_US_accents(text="यो॑ऽसि॒ सोऽसि॑") == "यो᳙ऽसि सो᳓ऽसि"
  assert accent.to_US_accents(text="म॒ही॒नाम्पयो॑ऽसि") == "महीना᳓म्प᳓योऽसि"
  # Leading accent mark does not raise IndexError in split_vyanjanas_and_svaras.
  assert accent.to_US_accents(text="॑सोऽकामयत") == "॑सोऽकामयत"
  telugu = sanscript.SCHEMES[sanscript.TELUGU]
  tel_in = sanscript.transliterate("यो॑ऽपां पुष्पव्ँ॒ वेद॑", sanscript.DEVANAGARI, sanscript.TELUGU)
  tel_us = accent.to_US_accents(text=tel_in, scheme=telugu)
  assert sanscript.transliterate(tel_us, sanscript.TELUGU, sanscript.DEVANAGARI) == "यो᳙ऽपां᳓ पु᳓ष्पव्ँ वे᳓द"


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


def test_fix_kAThaka_notation():
  sample = "य॑त्प्राण॑द्वायु॑रक्षितम् प्रसवे᳙ऽश्वि॑नोर् वीर्या᳗वन्तं +++(कुहू᳚र्देवा॑नाम्)+++"
  expected = "य᳓त्प्राण᳓द्वायु᳓रक्षितम् प्रसवे᳙ऽश्वि᳓नोर् वीर्या᳙वन्तं +++(कुहू᳙र्देवा᳓नाम्)+++"
  assert accent.fix_kAThaka_notation(sample) == expected
  assert accent.from_US_to_kAThaka_notation(expected) == "य॑त्प्राण॑द्वायु॑रक्षितम् प्रसवे᳙ऽश्वि॑नोर् वीर्या᳙वन्तं +++(कुहू᳙र्देवा॑नाम्)+++"


def test_to_US_accents_atharva_kampa_pluta():
  # Atharvavedic independent svarita ᳡ (including post-᳡ anudatta ॑ dip and redundant ॑᳡)
  assert accent.to_US_accents("अ॒न्यत्रा॒स्मन्न्यु᳡च्यतु") == "अन्य᳓त्रास्म᳓न्न्यु᳙च्यतु"
  assert accent.to_US_accents("दे॒वाना॑ममृतग॒र्भो᳡ऽसि॑ स्वप्न") == "देवा᳓नाममृतगर्भो᳙ऽसि स्वप्न"
  assert accent.to_US_accents("यस्ये॒दमा रजो॒ युज॑स्तु॒जे जना॒ वनं॒ स्वः॑᳡।") == "य᳓स्येद᳓मा᳓ र᳓जो यु᳓जस्तुजे᳓ ज᳓ना व᳓नं स्वः᳙।"
  # Hrasva and dirgha kampa (१ / ३) -> SVARITA_NEW + forward UDATTA paint
  assert accent.to_US_accents("अ॒प्स्व॑१न्तर॒मृत॑म॒प्सु भे॑ष॒जम्।") == "अप्स्व᳙न्त᳓रमृ᳓तमप्सु᳓ भेषज᳓म्।"
  assert accent.to_US_accents("शं न॒ आपो॑ धन्व॒न्या॑३॒॑ शमु॑ सन्त्वनू॒प्याः॑।") == "शं᳓ न आ᳓पो धन्वन्या᳙ श᳓मु सन्त्वनूप्याः᳙।"
  assert accent.to_US_accents("तेना॑ ते त॒न्वे॑३ शं क॑रम्") == "ते᳓ना ते तन्वे᳙ शं᳓ करम्"
  assert accent.to_US_accents("यो व॑ आपो॒ऽपां भा॒गो॒३॒॑प्स्व॒न्तर्य॑जु॒ष्यो᳡") == "यो᳓ व आपोऽपां᳓ भागो᳙प्स्वन्त᳓र्यजुष्यो᳙"
  assert accent.to_US_accents("स ए॒व मृ॒त्युः सो॒३॒॑मृतं॒ सो॒३॒॑भ्वं१॒॑ स रक्षः॑ ॥") == "स᳓ एव᳓ मृत्युः᳓ सो᳙मृ᳓तं सो᳙भ्वं᳙ स᳓ र᳓क्षः ॥"
  assert accent.to_US_accents("अग॑न्म॒ स्वः१॒॑स्व᳡रगन्म॒ सं") == "अ᳓गन्म स्वः᳙स्व᳙रगन्म सं᳓"
  assert accent.to_US_accents("आ॒रे॑३ ऽसा॑व॒स्मद॑स्तु") == "आरे᳙ ऽसा᳓वस्म᳓दस्तु"
  # True pluta ३ is preserved (both unmarked and dependent-svarita before sannatara/pause)
  assert accent.to_US_accents("ख॑ण्व॒खा३इ॑ खैम॒खा३इ॒ मध्ये॑", pauses=r"[।॥,;]+") == "ख᳙ण्वखा᳓३इ खैमखा᳓३इ म᳓ध्ये"
  assert accent.to_US_accents("क्षि॒प्रं वै तस्य॑ पृच्छन्ति॒ यत्तदासी॑३दि॒दं नु ता३दिति॑ ॥") == "क्षिप्रं᳓ वै᳓ त᳓स्य पृच्छन्ति य᳓त्त᳓दा᳓सी३दिदं᳓ नु᳓ ता᳓३दि᳓ति ॥"
  # Wrapped odd padas without danda when pauses excludes newline
  assert accent.to_US_accents("भ॒द्रा ह्य् अ᳡स्याः॒ प्रम॑तिर् ब॒भूव॒\nसेमं य॒ज्ञम् **अ॑वतु** दे॒व-गो॑पा ॥", pauses=r"[।॥,;]+") == "भद्रा᳓ ह्य् अ᳙स्याः प्र᳓मतिर् बभू᳓व\nसे᳓मं᳓ यज्ञ᳓म् **अवतु** देव᳓-गोपा ॥"



def test_to_US_accents_rigveda_kampa_visarga_and_pluta():
  # Rigveda kampa followed by visarga keeps visarga and converts kampa to ᳙
  assert accent.to_US_accents("त॒न्व१॑ः॒ सुजा॑ताः") == "तन्वः᳙ सु᳓जाताः"
  # Rigveda pluta ३ with chandrabindu stays intact
  assert accent.to_US_accents("न त्वा॒ भीरि॑व विन्दती३ँ ॥") == "न᳓ त्वा भी᳓रिव विन्दती३ँ ॥"
