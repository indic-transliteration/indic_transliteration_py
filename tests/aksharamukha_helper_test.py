import importlib

import pytest
import sys


pytest.importorskip("aksharamukha", reason="The aksharamukha library is required for these tests.")
from indic_transliteration import aksharamukha_helper

def test_transliterate_tamil():
  assert aksharamukha_helper.transliterate_tamil("அற்று") == "अऱ्ऱु"
    