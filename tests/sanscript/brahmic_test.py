from indic_transliteration import sanscript
from indic_transliteration.sanscript.schemes import VisargaApproximation


def test_force_lazy_anusvaara_devanagari():
  assert sanscript.SCHEMES[sanscript.KANNADA].force_lazy_anusvaara("ತನ್ತು") == "ತಂತು"
  assert sanscript.SCHEMES[sanscript.KANNADA].force_lazy_anusvaara("ಅಂಕ") == "ಅಂಕ"


def test_fix_lazy_anusvaara_devanagari():
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("किंच", ignore_padaanta=True,
                                                                    omit_yrl=True) == "किञ्च"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("संविकटमेव", omit_sam=True) == "संविकटमेव"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("तं जित्वा") == "तं जित्वा"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("जगइ") == "जगइ"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("षष्टं विकटमेव",
                                                                    ignore_padaanta=False) == "षष्टव्ँ विकटमेव"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("षष्टं विकटमेव", omit_yrl=True) == "षष्टं विकटमेव"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("षष्ठं विकंटमेव",
                                                                    ignore_padaanta=True) == "षष्ठं विकण्टमेव"


def test_fix_lazy_visarga():
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः पश्य") == "अन्तᳶ पश्य"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः कुरु") == "अन्तᳵ कुरु"



def test_approximate_visarga():
  assert sanscript.SCHEMES[sanscript.KANNADA].approximate_visargas("ಮತಿಃ", mode=VisargaApproximation.H) == "ಮತಿಹ್"
  assert sanscript.SCHEMES[sanscript.KANNADA].approximate_visargas("ಹರಃ", mode=VisargaApproximation.H) == "ಹರಹ್"
  assert sanscript.SCHEMES[sanscript.KANNADA].approximate_visargas("ಮತಿಃ", mode=VisargaApproximation.AHA) == "ಮತಿಹಿ"
  assert sanscript.SCHEMES[sanscript.KANNADA].approximate_visargas("ಹರಃ", mode=VisargaApproximation.AHA) == "ಹರಹ"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].approximate_visargas("मतिः", mode=VisargaApproximation.H) == "मतिह्"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].approximate_visargas("हरः", mode=VisargaApproximation.H) == "हरह्"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].approximate_visargas("मतिः", mode=VisargaApproximation.AHA) == "मतिहि"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].approximate_visargas("हरः", mode=VisargaApproximation.AHA) == "हरह"


def test_do_vyanjana_svara_join():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.do_vyanjana_svara_join("ह्र्", "ईः") == "ह्रीः"
  assert sanscript.SCHEMES[sanscript.KANNADA].do_vyanjana_svara_join("ಹ್ರ್", "ಈಃ") == "ಹ್ರೀಃ"


def test_split_vyanjanas_and_svaras():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.split_vyanjanas_and_svaras("नु॑") == ['न्', 'उ॑']
  assert devanagari.split_vyanjanas_and_svaras("सोऽग्नि᳘मेॗव") == ['स्', "ओ", 'ऽ', 'ग्', "न्", "इ᳘", "म्", "एॗ", "व्", "अ"]
  assert devanagari.split_vyanjanas_and_svaras("मं") == ['म्', 'अं']
  assert devanagari.split_vyanjanas_and_svaras("ह्रीः") == ['ह्', 'र्', 'ईः']
  assert sanscript.SCHEMES[sanscript.KANNADA].split_vyanjanas_and_svaras("ಹ್ರೀಃ") == ["ಹ್", "ರ್", "ಈಃ"]
  assert devanagari.split_vyanjanas_and_svaras("ह्र") == ['ह्', 'र्', 'अ']
  assert devanagari.split_vyanjanas_and_svaras("र") == ['र्', 'अ']
  assert devanagari.split_vyanjanas_and_svaras("द॒") == ['द्', 'अ॒']


def test_join_post_viraama():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.join_post_viraama("दिष्टा यत्रानधीते मुनिभिर् अनघता तत्र तत्-कर्तृतोक्ता  \nप्रोक्तं ब्रह्म स्वयंभ्व् इत्यपि जनि-विलयाभावम् अत्र स्मरन्ति ॥ १६५ ॥") == 'दिष्टा यत्रानधीते मुनिभिरनघता तत्र तत्कर्तृतोक्ता  \nप्रोक्तं ब्रह्म स्वयंभ्वित्यपि जनिविलयाभावमत्र स्मरन्ति ॥ १६५ ॥'
  assert devanagari.join_post_viraama("प्रोक्तं ब्रह्म स्वयंभ्व् इत्यपि जनि-विलयाभावमत्र स्मरन्ति") == "प्रोक्तं ब्रह्म स्वयंभ्वित्यपि जनिविलयाभावमत्र स्मरन्ति"
  assert devanagari.join_post_viraama("पश्चात् तु ज्ञानशक्त्योर् अपचयनियमाद् व्यासकॢप्तिस् समीची") == "पश्चात्तु ज्ञानशक्त्योरपचयनियमाद्व्यासकॢप्तिस्समीची"


def test_join_letters():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.join_strings(['ह्', 'र्', 'ईः']) == "ह्रीः"
  assert devanagari.join_strings(['ह्', 'र्', 'अ']) == "ह्र"
  assert sanscript.SCHEMES[sanscript.KANNADA].join_strings(["ಹ್", "ರ್", "ಈಃ"]) == "ಹ್ರೀಃ"


def test_apply_roman_numerals():
  devanagari_str = "हरि बोल १ ३ ५४ ६ ९को"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].apply_roman_numerals(devanagari_str) == "हरि बोल 1 3 54 6 9को"
  tamil_str = 'உந்து~மதக்களிற்றன்'
  assert sanscript.SCHEMES[sanscript.TAMIL].apply_roman_numerals(tamil_str) == tamil_str


def test_dot_for_numeric_ids():
  devanagari_str = "हरि बोल १।३।५४ ६ ९को"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].dot_for_numeric_ids(devanagari_str) == "हरि बोल १.३.५४ ६ ९को"
