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

def test_itrans_to_optitrans():
    assert sanscript.itrans_to_optitrans("sha~Nkara") == "shankara"
    assert sanscript.itrans_to_optitrans("ma~njIra") == "manjIra"

