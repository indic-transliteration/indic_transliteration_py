from indic_transliteration import sanscript



def test_fix_lazy_anusvaara_devanagari():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("तं जित्वा") == "तञ् जित्वा"

def test_fix_lazy_visarga():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः पश्य") == "अन्तᳶ पश्य"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः कुरु") == "अन्तᳵ कुरु"

def test_do_vyanjana_svara_join():
    devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
    assert devanagari.do_vyanjana_svara_join("ह्र्", "ईः") == "ह्रीः"
    