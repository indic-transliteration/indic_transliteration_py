# -*- coding: utf-8 -*-
"""
test.sanscript
~~~~~~~~~~~~~~

Tests Sanskrit transliteration.

:license: MIT and BSD
"""

from __future__ import unicode_literals

import logging

import pytest
import os
import json
from indic_transliteration import sanscript
# Remove all handlers associated with the root logger object.
from indic_transliteration.sanscript.schemes import roman

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



def _compare_all_data_between_schemes(_from, _to):
  """Compare all data for `_from` and `_to`"""
  DATA = test_data["basic_all_to_all"]
  if _from not in DATA or _to not in DATA:
    return 
  def compare_group(_from, _to, group):
    """Compare data for `_from` and `_to` in the test group `group`."""
    source = DATA[_from][group]
    actual = ' '.join(sanscript.transliterate(source, _from, _to).split())
    expected = ' '.join(DATA[_to][group].split())
    assert expected == actual, "Failure ahoy: %s to %s: expected %s, got %s" % (_from, _to, expected, actual)

  for group in DATA[_from]:
    if _to in DATA and group in DATA[_to]:
      compare_group(_from, _to, group)



@pytest.mark.parametrize("name", sanscript.SCHEMES)
def test_membership(name):
  """Test that a scheme is roman iff `is_roman`"""
  assert sanscript.SCHEMES[name].is_roman == (name in roman.ALL_SCHEME_IDS)


@pytest.mark.parametrize("name,scheme", sanscript.SCHEMES.items())
def test_correspondence(name, scheme ):
  """Test that schemes correspond to a subset of Devanagari.

  Since Devanagari is the most comprehensive scheme available, every
  scheme corresponds to a subset of Devanagari."""
  dev = sanscript.SCHEMES[sanscript.DEVANAGARI]
  groups = set(dev.keys())
  for group in scheme:
    logging.debug(name)
    logging.debug(group)
    if group not in ["accented_vowel_alternates", "extra_consonants", "candra", "zwj", 'zwnj', "skip", "shortcuts"] and not group.startswith("_"):
      assert group in groups


@pytest.mark.parametrize("from_scheme", roman.ALL_SCHEME_IDS)
@pytest.mark.parametrize("to_scheme", roman.ALL_SCHEME_IDS)
def test_to_roman(from_scheme, to_scheme):
  """Test roman to roman."""
  _compare_all_data_between_schemes(from_scheme, to_scheme)


@pytest.mark.parametrize("from_scheme", roman.ALL_SCHEME_IDS)
@pytest.mark.parametrize("to_scheme", sanscript.brahmic.SCHEMES.keys())
def test_to_brahmic(from_scheme, to_scheme):
  """Test roman to Brahmic."""
  _compare_all_data_between_schemes(from_scheme, to_scheme)


def test_devanaagarii_equivalence():
  """Test all synonmous transliterations."""
  logging.info(sanscript.transliterate("rAmo gUDhaM vaktI~Ngitaj~naH kShetre", sanscript.ITRANS, sanscript.DEVANAGARI))
  assert sanscript.transliterate("rAmo gUDhaM vaktI~Ngitaj~naH kShetre", sanscript.ITRANS, sanscript.DEVANAGARI) == \
                   sanscript.transliterate("raamo guuDhaM vaktii~NgitaGYaH xetre", sanscript.ITRANS, sanscript.DEVANAGARI)


@pytest.mark.parametrize("to_scheme", roman.ALL_SCHEME_IDS)
def test_brahmic_to_roman(to_scheme):
  """Test Brahmic to roman."""
  from_scheme = sanscript.DEVANAGARI
  _compare_all_data_between_schemes(from_scheme, to_scheme)


@pytest.mark.parametrize("to_scheme", sanscript.brahmic.SCHEMES.keys())
def test_devanagari_to_brahmic(to_scheme):
  """Test Brahmic to Brahmic."""
  from_scheme = sanscript.DEVANAGARI
  _compare_all_data_between_schemes(from_scheme, to_scheme)

@pytest.mark.parametrize("scheme_id", sanscript.brahmic.SCHEMES.keys())
def test_vowel_to_mark_map(scheme_id):
  brahmic_scheme = sanscript.SCHEMES[scheme_id]
  assert brahmic_scheme.from_devanagari("अ") not in brahmic_scheme.vowel_to_mark_map
  assert brahmic_scheme.vowel_to_mark_map[brahmic_scheme.from_devanagari("आ")] == brahmic_scheme.from_devanagari("ा")
  for vowel in "इ ई उ ऊ ए ऐ ओ औ".split(" "):
    assert brahmic_scheme.vowel_to_mark_map[brahmic_scheme.from_devanagari(vowel)] == brahmic_scheme.from_devanagari(sanscript.SCHEMES[sanscript.DEVANAGARI].vowel_to_mark_map[vowel]), vowel

## Toggle tests
def _toggle_test_helper(_from, _to):
  def func(data, output):
    assert output == sanscript.transliterate(data, _from, _to,  togglers= {'##'}, suspend_on= set('<'), suspend_off = set('>')), "_from: %s, _to: %s, _input: %s" % (_from, _to, data)

  return func

def test_toggle():
  f = _toggle_test_helper(sanscript.HK, sanscript.DEVANAGARI)
  f('akSa##kSa##ra', 'अक्षkSaर')
  f('##akSa##kSa##ra', 'akSaक्षra')
  f('akSa##ra##', 'अक्षra')
  f('akSa##ra', 'अक्षra')
  f('akSa##kSa##ra####', 'अक्षkSaर')
  f('a####kSara', 'अक्षर')
  f('a#kSara', 'अ#क्षर')

def test_suspend():
  f = _toggle_test_helper(sanscript.HK, sanscript.DEVANAGARI)
  f('<p>nara iti</p>', '<p>नर इति</p>')

def test_suspend_and_toggle():
  f = _toggle_test_helper(sanscript.HK, sanscript.DEVANAGARI)
  f('<p>##na##ra## iti</p>', '<p>naर iti</p>')

