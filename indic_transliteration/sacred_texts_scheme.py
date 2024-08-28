"""
Deal with the idiosyncratic transliteration scheme used by "Sacred texts of the east" type publishers from around 1900.
"""
import logging


def decode_italicized_text(text):
    if len(text) > 2:
        logging.warning("Beware! usually not an encoded sanskrit text")
    replacements = {"n": "ṇ", "t": "ṭ", "d": "ḍ", "m": "ṁ", "kh": "ch", "h": "ḥ", "ri": "r̥", "k": "c", "g": "j", "s": "ś"} # sh not intalicized is ṣ
    for x, y in replacements.items():
        text = text.replace(x, y)
        text = text.replace(x.capitalize(), y.capitalize())
    return text


def decode_nonitalicized(text):
  replacements = {"â": "ā", "î": "ī", "û": "ū", "": "\\`", "": " - ", " ": " "}
  for x, y in replacements.items():
    text = text.replace(x, y)
    text = text.replace(x.capitalize(), y.capitalize())
  return text