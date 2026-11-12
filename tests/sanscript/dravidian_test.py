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



def test_malayalam_chillu_letters():
  # Chillu letters are bare consonants. They were not in the map and leaked through.
  assert sanscript.transliterate("അവൻ", sanscript.MALAYALAM, sanscript.IAST) == "avan"
  assert sanscript.transliterate("അവൻ", sanscript.MALAYALAM, sanscript.DEVANAGARI) == "अवन्"
  assert sanscript.transliterate("കാർ", sanscript.MALAYALAM, sanscript.IAST) == "kār"
  # Every chillu must equal its explicit consonant + virama spelling.
  from indic_transliteration.sanscript.schemes.brahmic import MalayalamScheme
  for chillu, base in MalayalamScheme.CHILLU.items():
    for to in (sanscript.IAST, sanscript.DEVANAGARI):
      assert sanscript.transliterate("അ" + chillu, sanscript.MALAYALAM, to) == sanscript.transliterate("അ" + base, sanscript.MALAYALAM, to)
  assert sanscript.transliterate("മെഡിക്കൽ", sanscript.MALAYALAM, sanscript.IAST) == "mèḍikkal"
  # Old encoding: consonant + virama + ZWJ.
  assert sanscript.transliterate("അവന്‍", sanscript.MALAYALAM, sanscript.IAST) == "avan"
