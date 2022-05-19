from indic_transliteration import sanscript


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


def test_do_vyanjana_svara_join():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.do_vyanjana_svara_join("ह्र्", "ईः") == "ह्रीः"
  assert sanscript.SCHEMES[sanscript.KANNADA].do_vyanjana_svara_join("ಹ್ರ್", "ಈಃ") == "ಹ್ರೀಃ"


def test_split_vyanjanas_and_svaras():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.split_vyanjanas_and_svaras("ह्रीः") == ['ह्', 'र्', 'ईः']
  assert sanscript.SCHEMES[sanscript.KANNADA].split_vyanjanas_and_svaras("ಹ್ರೀಃ") == ["ಹ್", "ರ್", "ಈಃ"]
  assert devanagari.split_vyanjanas_and_svaras("ह्र") == ['ह्', 'र्', 'अ']
  assert devanagari.split_vyanjanas_and_svaras("र") == ['र्', 'अ']

def test_join_letters():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert devanagari.join_strings(['ह्', 'र्', 'ईः']) == "ह्रीः"
  assert sanscript.SCHEMES[sanscript.KANNADA].join_strings(["ಹ್", "ರ್", "ಈಃ"]) == "ಹ್ರೀಃ"


def test_apply_roman_numerals():
  devanagari_str = "हरि बोल १ ३ ५४ ६ ९को"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].apply_roman_numerals(devanagari_str) == "हरि बोल 1 3 54 6 9को"
  tamil_str = 'உந்து~மதக்களிற்றன்'
  assert sanscript.SCHEMES[sanscript.TAMIL].apply_roman_numerals(tamil_str) == tamil_str


def test_dot_for_numeric_ids():
  devanagari_str = "हरि बोल १।३।५४ ६ ९को"
  assert sanscript.SCHEMES[sanscript.DEVANAGARI].dot_for_numeric_ids(devanagari_str) == "हरि बोल १.३.५४ ६ ९को"
