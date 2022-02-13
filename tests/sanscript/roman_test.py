from indic_transliteration import sanscript


def test_fix_lazy_anusvaara_itrans():
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("shaMkara") == "sha~Nkara"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMchara") == "sa~nchara"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("ShaMDa") == "ShaNDa"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("shAMta") == "shAnta"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("sAMba") == "sAmba"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMvara") == "sav.Nvara"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMyukta") == "say.Nyukta"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMyukta", omit_yrl=True) == "saMyukta"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMyukta", omit_sam=True) == "saMyukta"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMlagna") == "sal.Nlagna"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMlagna", omit_sam=True) == "saMlagna"
  assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("taM jitvA") == "taM jitvA"


def test_fix_lazy_anusvaara_slp():
  assert sanscript.SCHEMES[sanscript.SLP1].fix_lazy_anusvaara("aham") == "aham"
  assert sanscript.SCHEMES[sanscript.SLP1].fix_lazy_anusvaara("saMga") == "saNga"
  assert sanscript.SCHEMES[sanscript.SLP1].fix_lazy_anusvaara("saMga", omit_sam=True) == "saMga"


def test_optitrans_to_lay_indian():
  assert sanscript.SCHEMES[sanscript.OPTITRANS].to_lay_indian("taM jitvA") == "tam jitva"
  assert sanscript.SCHEMES[sanscript.OPTITRANS].to_lay_indian("kRShNa") == "krishna"


def test_get_standard_form():
  assert sanscript.SCHEMES[sanscript.IAST].get_standard_form("dŕ̥ṃhasva") == "dṛ́ṃhasva"
  assert sanscript.SCHEMES[sanscript.IAST].get_standard_form("pitŕ̥̄ṃs") == "pitṝ́ṃs"


def test_to_double_lettered():
  assert sanscript.SCHEMES[sanscript.OPTITRANS].get_double_lettered("taM jitvA pUraya") == "taM jitvaa puuraya"


def test_mark_off_non_indic_in_line():
  text = '05 The Śaivas’ Inclusivist View of Their Own and the Vaidikas’ Religion'
  assert sanscript.SCHEMES[sanscript.IAST].mark_off_non_indic_in_line(
    text) == "<05> <The> Śaivas’ <Inclusivist> <View> <of> <Their> <Own> <and> <the> <Vaidikas’> <Religion>"

  assert sanscript.SCHEMES[sanscript.IAST].mark_off_non_indic_in_line(
    "02 Sources of Dharma") == "<02> <Sources> <of> <Dharma>"


def test_optitrans_from_urdu():
  optitrans_scheme = sanscript.SCHEMES[sanscript.OPTITRANS]
  test_pairs = {"lućpanaʼī": "luchpana{}ii",
                "marg̠-zār": "marga-zaara",
                "mūtā'ba‘at": "muutaabaata",
                "nis̱ẖās'tah": "nishaastaha",
                "laḵẖlaḵẖa": "la.khla.kha",
                "ifā'qā": "ifaaqaa",
                "nāṣěḥ": "naasEha",
                "ba-jāë": "ba-jaaE",
                "pes̱ẖ": "pesha",
                "joban": "jobana",
                "mad'ḥ": "mad{}ha",
                "pooṅc̱ẖh": "puu.NCha",
                "āzmā'’is̱ẖ": "aazmaa{}isha"
                }
  for source, dest in test_pairs.items():
    assert optitrans_scheme.approximate_from_iso_urdu(source) == dest, (source, dest)
  assert optitrans_scheme.approximate_from_iso_urdu("maẕhab", add_terminal_a=False) == "mazhab"
