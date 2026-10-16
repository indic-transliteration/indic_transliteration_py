import json
import os
import pytest
import logging

from indic_transliteration import sanscript

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s"
)



TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transliterationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
    # noinspection PyRedeclaration
    test_data = json.loads(test_data_file.read())
logging.info(test_data["dravidian_tests"])


@pytest.mark.parametrize("test_conversions", test_data["dravidian_tests"])
def test_to_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script == "dev" or (script not in sanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        transliteration = sanscript.transliterate(text, script, sanscript.DEVANAGARI)
        assert transliteration == dev_string, "Failed to convert " + script + " to devanAgarI. Compare: " + transliteration + " vs " + dev_string

@pytest.mark.parametrize("test_conversions", test_data["dravidian_tests"])
def test_from_devanagari(test_conversions):
    logging.debug(str(test_conversions))
    dev_string = test_conversions["dev"]
    for (script, text) in test_conversions.items():
        if script == "dev" or (script not in sanscript.SCHEMES.keys()):
            logging.debug("Skipping over script - " + script)
            continue
        transliteration = sanscript.transliterate(dev_string, sanscript.DEVANAGARI, script)
        assert transliteration == text, "Failed to convert to " + script + " from devanAgarI. Compare: " + transliteration + " vs " + text



def test_unmarked_tamil_consonants_map_to_first_varga_member():
  # Tamil writes all four of क ख ग घ as க (likewise ச ட த ப). When such a many-to-one
  # scheme is used as the SOURCE, the reverse map used to keep the LAST key, so a plain
  # க came back as घ / gha. The unmarked letter should map to the first member.
  assert sanscript.transliterate("கடை", sanscript.TAMIL, sanscript.DEVANAGARI) == "कटै"
  assert sanscript.transliterate("கடை", sanscript.TAMIL, sanscript.IAST) == "kaṭai"
  assert sanscript.transliterate("பாகம்", sanscript.TAMIL, sanscript.IAST) == "pākaṃ"
  assert sanscript.transliterate("சுதர்சன்", sanscript.TAMIL, sanscript.HK) == "cutarcan2"
  # The disambiguated schemes are unaffected.
  assert sanscript.transliterate("க²", sanscript.TAMIL_SUP, sanscript.DEVANAGARI) == "ख"
