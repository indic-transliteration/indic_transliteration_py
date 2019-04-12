import json
import logging
import os

import pytest

from indic_transliteration import sanscript

# Remove all handlers associated with the root logger object.

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(filename)s:%(lineno)d %(message)s"
)


TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'transliterationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
    # noinspection PyRedeclaration
    test_data = json.loads(test_data_file.read())
# logging.info(test_data["tests"])


SCRIPT_NAME_MAP= {
    "hk_sanscript": sanscript.HK
}


@pytest.mark.parametrize("test_conversions", test_data["to_devanaagarii"])
def test_to_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script in SCRIPT_NAME_MAP.keys():
            script = SCRIPT_NAME_MAP[script]
        if script == "dev" or (script not in sanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        result = sanscript.transliterate(text, script, sanscript.DEVANAGARI)
        assert dev_string == result, "Failed to convert " + script + " to devanAgarI: got " + result + " instead of " + dev_string


@pytest.mark.parametrize("test_conversions", test_data["from_devanaagarii"])
def test_from_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, expected_text) in test_conversions.items():
        if script in SCRIPT_NAME_MAP.keys():
            script = SCRIPT_NAME_MAP[script]
        if script in "dev" or (script not in sanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        result = sanscript.transliterate(dev_string, sanscript.DEVANAGARI, script)
        assert expected_text == result, "Failed to convert to " + script + " from devanAgarI: got " + result + " instead of " + expected_text


def test_optitrans_to_itrans():
    assert sanscript.transliterate("shankara", sanscript.OPTITRANS, sanscript.ITRANS) == "sha~Nkara"
    assert sanscript.transliterate("manjIra", sanscript.OPTITRANS, sanscript.ITRANS) == "ma~njIra"
    assert sanscript.transliterate("praBA", sanscript.OPTITRANS, sanscript.ITRANS) == "prabhA"
    assert sanscript.transliterate("pRRS", sanscript.OPTITRANS, sanscript.ITRANS) == "pRRISh"
    assert sanscript.transliterate("pRcCa", sanscript.OPTITRANS, sanscript.ITRANS) == "pRRichCha"
    assert sanscript.transliterate("R", sanscript.OPTITRANS, sanscript.ITRANS) == "RRi"
    assert sanscript.transliterate("Rc", sanscript.OPTITRANS, sanscript.ITRANS) == "RRich"

def test_itrans_to_optitrans():
    assert sanscript.transliterate("sha~Nkara", sanscript.ITRANS, sanscript.OPTITRANS) == "shankara"
    assert sanscript.transliterate("ma~njIra", sanscript.ITRANS, sanscript.OPTITRANS) == "manjIra"

def test_optitrans_to_lay_indian():
    assert sanscript.SCHEMES[sanscript.OPTITRANS].to_lay_indian("taM jitvA") == "tam jitva"
    assert sanscript.SCHEMES[sanscript.OPTITRANS].to_lay_indian("kRShNa") == "krishna"


def test_fix_lazy_anusvaara_itrans():
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("shaMkara") == "sha~Nkara"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMchara") == "sa~nchara"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("ShaMDa") == "ShaNDa"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("shAMta") == "shAnta"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("sAMba") == "sAmba"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMvara") == "sav.Nvara"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMyukta") == "say.Nyukta"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("saMlagna") == "sal.Nlagna"
    assert sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara("taM jitvA") == "ta~n jitvA"

def test_fix_lazy_anusvaara_devanagari():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_anusvaara("तं जित्वा") == "तञ् जित्वा"

def test_fix_lazy_visarga():
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः पश्य") == "अन्तᳶ पश्य"
    assert sanscript.SCHEMES[sanscript.DEVANAGARI].fix_lazy_visarga("अन्तः कुरु") == "अन्तᳵ कुरु"
    