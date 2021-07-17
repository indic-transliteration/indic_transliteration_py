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


TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transliterationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
    # noinspection PyRedeclaration
    test_data = json.loads(test_data_file.read())
# logging.info(test_data["tests"])


SCRIPT_NAME_MAP= {
    "hk_sanscript": sanscript.HK
}


def get_test_cases(test_tuples, ignored_cases=None):
    ignored_cases = ignored_cases or []
    test_cases = []
    for test_tuple in test_tuples:
        if "python/indic_transliteration" in test_tuple.get("nonSupportingPrograms", []):
            continue
        for script in test_tuple.keys():
            if script in SCRIPT_NAME_MAP.keys():
                script = SCRIPT_NAME_MAP[script]
            if script in sanscript.SCHEMES.keys() and script not in ["description", "dev"]:
                test_case = {"script": script, "text": test_tuple[script], "dev_string": test_tuple["dev"]}
                if test_tuple["dev"] in ignored_cases:
                    test_cases.append(pytest.param(test_case, marks=pytest.mark.xfail(reason="TODO")))
                else:
                    test_cases.append(test_case)
    return test_cases


test_tuples = test_data["to_devanaagarii"] + test_data["devanaagarii_round_trip"]
test_cases_to_dev = get_test_cases(test_tuples=test_tuples, ignored_cases=[])

@pytest.mark.parametrize("test_case", test_cases_to_dev)
def test_to_devanagari(test_case):
    logging.debug(str(test_case))
    dev_string = test_case["dev_string"]
    script = test_case["script"]
    text = test_case["text"]
    result = sanscript.transliterate(text, script, sanscript.DEVANAGARI)
    assert result == dev_string, "Failed to convert " + script + " to devanAgarI: got " + result + " instead of " + dev_string


test_tuples = test_data["from_devanaagarii"]\
              + test_data["devanaagarii_round_trip"]
ignored_cases = []
test_cases_from_dev = get_test_cases(test_tuples=test_tuples, ignored_cases=ignored_cases)

@pytest.mark.parametrize("test_case", test_cases_from_dev)
def test_from_devanagari(test_case):
    dev_string = test_case["dev_string"]
    script = test_case["script"]
    expected_text = test_case["text"]
    # logging.debug("Converting %s, expecting %s in %s" % (dev_string, expected_text, script))
    if script in SCRIPT_NAME_MAP.keys():
        script = SCRIPT_NAME_MAP[script]
    if script in "dev" or (script not in sanscript.SCHEMES.keys()):
        logging.debug("Skipping over script - " + script)
        return 
    result = sanscript.transliterate(dev_string, sanscript.DEVANAGARI, script)
    result_dev = sanscript.transliterate(result, script, sanscript.DEVANAGARI)
    assert expected_text == result or dev_string==result_dev, "Failed to convert to " + script + " from devanAgarI: got " + result + " instead of " + expected_text


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

