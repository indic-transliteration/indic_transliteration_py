import json
import os
import pytest
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)

from indic_transliteration import xsanscript

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dravidianTransliterationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
    # noinspection PyRedeclaration
    test_data = json.loads(test_data_file.read())
logging.info(test_data["tests"])


SCRIPT_NAME_MAP= {
    "hk_sanscript": xsanscript.HK
}


@pytest.mark.parametrize("test_conversions", test_data["tests"])
def test_to_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script in SCRIPT_NAME_MAP.keys():
            script = SCRIPT_NAME_MAP[script]
        if script == "dev" or (script not in xsanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        assert xsanscript.transliterate(text, script, xsanscript.DEVANAGARI) == dev_string, "Failed to convert " + script + " to devanAgarI"

@pytest.mark.parametrize("test_conversions", test_data["tests"])
def test_from_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script in SCRIPT_NAME_MAP.keys():
            script = SCRIPT_NAME_MAP[script]
        if script == "dev" or (script not in xsanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        transliteration = xsanscript.transliterate(dev_string, xsanscript.DEVANAGARI, script)
        assert transliteration == text, "Failed to convert to " + script + " from devanAgarI. Compare: " + transliteration + " vs " + text

