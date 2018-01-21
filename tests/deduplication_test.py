import json
import os
import pytest
import logging

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s %(message)s"
)

from indic_transliteration.sanscript import get_approx_deduplicating_key

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'approxDeduplicationTests.json')

test_data = {}
with open(TEST_DATA_PATH) as test_data_file:
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

