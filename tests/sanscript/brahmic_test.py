from indic_transliteration import sanscript


def test_optitrans_to_lay_indian():
    assert sanscript.SCHEMES[sanscript.OPTITRANS].to_lay_indian("taM jitvA") == "tam jitva"
    assert sanscript.SCHEMES[sanscript.OPTITRANS].to_lay_indian("kRShNa") == "krishna"


def test_fix_lazy_anusvaara_devanagari():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("तं जित्वा") == "तञ् जित्वा"

def test_fix_lazy_visarga():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः पश्य") == "अन्तᳶ पश्य"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः कुरु") == "अन्तᳵ कुरु"
