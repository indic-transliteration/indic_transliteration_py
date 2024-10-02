import importlib

import pytest
import sys

from indic_transliteration import aksharamukha_helper



@pytest.mark.skipif(
  not importlib.util.find_spec("aksharamukha"), reason="requires the aksharamukha library")
def test_transliterate_tamil():
  assert aksharamukha_helper.transliterate_tamil("அற்று") == "अऱ्ऱु"
    