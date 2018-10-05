import json
import os
import pytest
import logging

from indic_transliteration import deduplication

from indic_transliteration.deduplication import get_approx_deduplicating_key

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s %(message)s"
)


TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'approxDeduplicationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
  # noinspection PyRedeclaration
  test_data = json.loads(test_data_file.read())
logging.info(test_data["duplicates"])


@pytest.mark.parametrize("duplicates", test_data["duplicates"])
def test_duplicates(duplicates):
  logging.debug(str(duplicates))
  keys = set(map(get_approx_deduplicating_key, duplicates))
  assert len(keys) == 1, str(duplicates) + "-----" + str(keys)

@pytest.mark.parametrize("non_duplicates", test_data["non_duplicates"])
def test_non_duplicates(non_duplicates):
  logging.debug(str(non_duplicates))
  keys = set(map(get_approx_deduplicating_key, non_duplicates))
  assert len(keys) > 1, str(non_duplicates) + "-----" + str(keys)


def test_fix_lazy_anusvaara_itrans():
  assert deduplication.fix_lazy_anusvaara_itrans("shaMkara") == "sha~Nkara"
  assert deduplication.fix_lazy_anusvaara_itrans("saMchara") == "sa~nchara"
  assert deduplication.fix_lazy_anusvaara_itrans("ShaMDa") == "ShaNDa"
  assert deduplication.fix_lazy_anusvaara_itrans("shAMta") == "shAnta"
  assert deduplication.fix_lazy_anusvaara_itrans("sAMba") == "sAmba"
  assert deduplication.fix_lazy_anusvaara_itrans("saMvara") == "sav.Nvara"
  assert deduplication.fix_lazy_anusvaara_itrans("saMyukta") == "say.Nyukta"
  assert deduplication.fix_lazy_anusvaara_itrans("saMlagna") == "sal.Nlagna"
  assert deduplication.fix_lazy_anusvaara_itrans("taM jitvA") == "ta~n jitvA"
