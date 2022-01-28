"""
Test conversion from integer to Roman numeral
"""

from typing import Any

import pytest
from roman import InvalidRomanNumeralError

from indic_transliteration.roman_numerals import convert_to_integer

from .parameters import LOWERCASE_PARAMETERS, STANDARD_PARAMETERS


@pytest.mark.parametrize(
  "expected_integer, roman_numeral",
  LOWERCASE_PARAMETERS + STANDARD_PARAMETERS)
def test_integer_conversion(
    roman_numeral: str, expected_integer: int,
) -> None:
  """
  Test conversion from integers to uppercase Unicode Roman numerals
  """
  assert convert_to_integer(roman_numeral) == expected_integer


@pytest.mark.parametrize("non_strings", [
  2,
  5.0,
  True,
  set(),
  {'hello': 4},
  lambda: print('called!'),  # pragma: no cover
])
def test_invalid_types(non_strings: Any) -> None:
  """
  Ensure that passing in non-strings results in Type exceptions
  """
  with pytest.raises(TypeError):
    convert_to_integer(non_strings)


@pytest.mark.parametrize("invalid_numerals", [
  '',
  'ⅠⅯ',
  'ⅰⅿ',
  'ⅠⅮ',
  'ⅰⅾ',
  'ⅠⅭ',
  'ⅰⅽ',
  'ⅠⅬ',
  'ⅰⅼ',
  'ⅬⅯ',
  'ⅼⅿ',
  'ⅮⅯ',
  'ⅾⅿ',
])
def test_invalid_numerals(invalid_numerals: Any) -> None:
  """
  Ensure that passing in invalid Roman numerals raises ValueErrors
  """
  with pytest.raises(InvalidRomanNumeralError):
    convert_to_integer(invalid_numerals)