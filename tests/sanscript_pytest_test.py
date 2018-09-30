import json
import os
import pytest
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)

from indic_transliteration import sanscript

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'transliterationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
    # noinspection PyRedeclaration
    test_data = json.loads(test_data_file.read())
logging.info(test_data["tests"])


SCRIPT_NAME_MAP= {
    "hk_sanscript": sanscript.HK
}


@pytest.mark.parametrize("test_conversions", test_data["tests"])
def test_to_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script in SCRIPT_NAME_MAP.keys():
            script = SCRIPT_NAME_MAP[script]
        if script == "dev" or (script not in sanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        assert sanscript.transliterate(text, script, sanscript.DEVANAGARI) == dev_string, "Failed to convert " + script + " to devanAgarI"


def test_optitrans_to_itrans():
    assert sanscript.optitrans_to_itrans("shankara") == "sha~Nkara"
    assert sanscript.optitrans_to_itrans("manjIra") == "ma~njIra"
    assert sanscript.optitrans_to_itrans("praBA") == "prabhA"
    assert sanscript.optitrans_to_itrans("pRRS") == "pRRISh"
    assert sanscript.optitrans_to_itrans("pRcCa") == "pRRichCha"
    assert sanscript.optitrans_to_itrans("R") == "RRi"
    assert sanscript.optitrans_to_itrans("Rc") == "RRich"

def test_itrans_to_optitrans():
    assert sanscript.itrans_to_optitrans("sha~Nkara") == "shankara"
    assert sanscript.itrans_to_optitrans("ma~njIra") == "manjIra"

def test_fix_lazy_anusvaara_itrans():
    assert sanscript.fix_lazy_anusvaara_itrans("shaMkara") == "sha~Nkara"
    assert sanscript.fix_lazy_anusvaara_itrans("saMchara") == "sa~nchara"
    assert sanscript.fix_lazy_anusvaara_itrans("ShaMDa") == "ShaNDa"
    assert sanscript.fix_lazy_anusvaara_itrans("shAMta") == "shAnta"
    assert sanscript.fix_lazy_anusvaara_itrans("sAMba") == "sAmba"
    assert sanscript.fix_lazy_anusvaara_itrans("saMvara") == "sav.Nvara"
    assert sanscript.fix_lazy_anusvaara_itrans("saMyukta") == "say.Nyukta"
    assert sanscript.fix_lazy_anusvaara_itrans("saMlagna") == "sal.Nlagna"
    assert sanscript.fix_lazy_anusvaara_itrans("taM jitvA") == "ta~n jitvA"
