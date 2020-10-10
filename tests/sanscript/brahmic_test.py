from indic_transliteration import sanscript



def test_fix_lazy_anusvaara_devanagari():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("संविकटमेव", omit_sam=True) == "संविकटमेव"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("तं जित्वा") == "तञ् जित्वा"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("जगइ") == "जगइ"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("षष्टं विकटमेव") == "षष्टव्ँ विकटमेव"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("षष्टं विकटमेव", omit_yrl=True) == "षष्टं विकटमेव"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("षष्ठं विकंटमेव",
                                                                      ignore_padaanta=True) == "षष्ठं विकण्टमेव"

def test_fix_lazy_visarga():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः पश्य") == "अन्तᳶ पश्य"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः कुरु") == "अन्तᳵ कुरु"

def test_do_vyanjana_svara_join():
    devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
    assert devanagari.do_vyanjana_svara_join("ह्र्", "ईः") == "ह्रीः"

def test_apply_roman_numerals():
    devanagari_str = "हरि बोल १ ३ ५४ ६ ९को"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].apply_roman_numerals(devanagari_str) == "हरि बोल 1 3 54 6 9को"