import regex


def move_accent_to_previous_syllable(scheme, text, old_accent, new_accent=None, drop_at_first_syllable=False):
  if new_accent is None:
    new_accent = old_accent
  letters = scheme.split_vyanjanas_and_svaras(text)
  out_letters = []
  vowels = list(scheme["vowels"].values())
  vowels_yogavaahas = vowels + list(scheme["yogavaahas"].values())
  accent_carryover = ""
  for index, letter in enumerate(letters):
    if letter.endswith(old_accent):
      vowel_position = -1
      for i in range(len(out_letters) - 1, -1, -1):
        prev_letter = out_letters[i]
        if prev_letter[0] in vowels_yogavaahas:
          vowel_position = i
          break
      if vowel_position == -1:
        if not drop_at_first_syllable:
          accent_carryover += new_accent
      else: 
        out_letters[vowel_position] += new_accent
      out_letters.append(letter[:-1])
    else:
      out_letters.append(letter)
  text = scheme.join_strings(out_letters)
  return accent_carryover + text


def to_shatapatha_svara(scheme, text):
  """
  Limitations: Does not handle eliding udAtta-s occuring in a series. It is assumed that such are pre-elided
  
  :param text: 
  :return: 
  """
  # References: https://en.wikipedia.org/wiki/Combining_Diacritical_Marks
  text = text.replace("꣡", "᳘")
  text = regex.sub("᳘([ंःँ])", "\\1᳘", text)
  text = regex.sub("[ँꣳ]", "ᳫं", text)
  # This would be wrong: text = text.replace("᳡", "ॗ") . Svarita is marked in the previous syllable.    
  new_accent = "ॗ"
  old_accent = "᳡"
  text = move_accent_to_previous_syllable(scheme=scheme, text=text, new_accent=new_accent, old_accent=old_accent)
  return text


def add_accent_to_end(scheme, text, accent="᳟"):
  letters = "".join(scheme.get_letters())
  text = regex.sub(f"([{letters}])([^{letters}]+)$", f"\\1{accent}\\2", text)
  return text
