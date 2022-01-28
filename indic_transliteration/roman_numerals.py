"""
Library to convert to and from Roman numerals in various encodings

Placed here till https://github.com/jambonrose/roman-numerals/pull/64 is accepted.
"""

from re import (
  VERBOSE, compile as re_compile, sub as substitute, )

# Operation Modes
import roman

MODE_STANDARD = 1
MODE_LOWERCASE = 2
MODE_ASCII = 3

ROMAN_NUMERAL_TABLE = [
  (1000, 'Ⅿ'),
  (900, 'ⅭⅯ'),
  (500, 'Ⅾ'),
  (400, 'ⅭⅮ'),
  (100, 'Ⅽ'),
  (90, 'ⅩⅭ'),
  (50, 'Ⅼ'),
  (40, 'ⅩⅬ'),
  (10, 'Ⅹ'),
  (9, 'Ⅸ'),
  (5, 'Ⅴ'),
  (4, 'Ⅳ'),
  (1, 'Ⅰ'),
]

SHORTENINGS = [
  ('ⅩⅠⅠ', 'Ⅻ'),
  ('ⅩⅠ', 'Ⅺ'),
  ('ⅠⅩ', 'Ⅸ'),
  ('ⅤⅠⅠⅠ', 'Ⅷ'),
  ('ⅤⅠⅠ', 'Ⅶ'),
  ('ⅤⅠ', 'Ⅵ'),
  ('ⅠⅤ', "Ⅳ"),
  ('ⅠⅠⅠ', 'Ⅲ'),
  ('ⅠⅠ', 'Ⅱ'),
]
STANDARD_TRANS = 'ⅯⅮⅭⅬⅫⅪⅩⅨⅧⅦⅥⅤⅣⅢⅡⅠ'
LOWERCASE_TRANS = 'ⅿⅾⅽⅼⅻⅺⅹⅸⅷⅶⅵⅴⅳⅲⅱⅰ'


def convert_to_numeral(decimal_integer: int, mode: int = MODE_ASCII) -> str:
  """Convert a decimal integer to a Roman numeral"""
  if (not isinstance(decimal_integer, int)
      or isinstance(decimal_integer, bool)):
    raise TypeError("decimal_integer must be of type int")
  if (not isinstance(mode, int)
      or isinstance(mode, bool)):
    raise ValueError(
      "mode not recognized"
    )
  return_list = []
  remainder = decimal_integer
  for integer, numeral in ROMAN_NUMERAL_TABLE:
    repetitions, remainder = divmod(remainder, integer)
    return_list.append(numeral * repetitions)
  numeral_string = ''.join(return_list)

  if mode == MODE_ASCII:
    numeral_string = roman_to_ascii(numeral_string=numeral_string)
  else:
    numeral_string = use_shortenings(numeral_string)

  if mode == MODE_LOWERCASE:
    trans_to_lowercase = str.maketrans(STANDARD_TRANS, LOWERCASE_TRANS)
    numeral_string = numeral_string.translate(trans_to_lowercase)
  return numeral_string


def use_shortenings(numeral_string):
  for full_string, shortening in SHORTENINGS:
    numeral_string = substitute(
      r'%s$' % full_string,
      shortening,
      numeral_string,
    )
  return numeral_string


NUMERAL_PATTERN = re_compile(
  """
  Ⅿ*                # thousands
  (ⅭⅯ|ⅭⅮ|Ⅾ?Ⅽ{0,3})  # hundreds - ⅭⅯ (900), ⅭⅮ (400), ⅮⅭⅭⅭ (800), ⅭⅭⅭ (300)
  (ⅩⅭ|ⅩⅬ|Ⅼ?Ⅹ{0,3})  # tens - ⅩⅭ (90), ⅩⅬ (40), ⅬⅩⅩⅩ (80), ⅩⅩⅩ (30)
  (Ⅸ|Ⅳ|Ⅴ?Ⅰ{0,3})   # ones - Ⅸ (9), Ⅳ (4), ⅤⅠⅠⅠ (8), ⅠⅠⅠ (3)
  """,
  VERBOSE
)


def convert_to_integer(roman_numeral: str) -> int:
  """Convert a Roman numeral to a decimal integer"""
  if not isinstance(roman_numeral, str):
    raise TypeError("decimal_integer must be of type int")
  if roman_numeral == '':
    raise roman.InvalidRomanNumeralError("roman_numeral cannot be an empty string")

  # ensure all characters are in the standard/uppercase set
  trans_to_uppercase = str.maketrans(LOWERCASE_TRANS, STANDARD_TRANS)
  # named partial_numeral because it will be shortened in loop below
  partial_numeral = roman_numeral.translate(trans_to_uppercase)

  partial_numeral = remove_shortenings(partial_numeral)
  partial_numeral = roman_to_ascii(numeral_string=partial_numeral)
  value = roman.fromRoman(partial_numeral)

  return value


def remove_shortenings(partial_numeral):
  # remove Unicode shortenings in favor of chars in conversion table
  for full_string, shortening in SHORTENINGS:
    partial_numeral = substitute(
      r'%s$' % shortening,
      full_string,
      partial_numeral,
    )
  return partial_numeral


roman_to_ascii_map = {"Ⅰ": "I", "Ⅴ": "V", "Ⅹ": "X", "Ⅼ": "L", "Ⅽ": "C", "Ⅾ": "D", "Ⅿ": "M"}


def roman_to_ascii(numeral_string):
  numeral_string = remove_shortenings(numeral_string)
  for rom, asc in roman_to_ascii_map.items():
    numeral_string = numeral_string.replace(rom, asc)
  return numeral_string



def ascii_to_roman(numeral_string):
  for rom, asc in roman_to_ascii_map.items():
    numeral_string = numeral_string.replace(asc, rom)
  numeral_string = use_shortenings(numeral_string)
  numeral_string.replace('ⅠⅤ', 'Ⅳ')
  return numeral_string


