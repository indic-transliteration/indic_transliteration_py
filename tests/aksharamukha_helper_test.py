import importlib

import pytest
import sys




@pytest.mark.skipif(
  not importlib.util.find_spec("aksharamukha"), reason="requires the aksharamukha library")
def test_transliterate_tamil():
  from indic_transliteration import aksharamukha_helper
  assert aksharamukha_helper.transliterate_tamil("அற்று") == "अऱ्ऱु"
    