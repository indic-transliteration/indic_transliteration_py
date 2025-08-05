import regex

ACCENTS_PATTERN = "[\u1CD0-\u1CE8\u1CF9\u1CFA\uA8E0-\uA8F1\u0951-\u0954\u0957]"  # included  ॗ , which is used as svara for weber's shatapatha


def add_accent_to_previous_syllable(scheme, text, old_accent, new_accent=None, drop_at_first_syllable=False,
                                    retain_old_accent=False):
  """
  modify text by moving old_accent from its current position to the preceding syllable's vowel or yogavaaha (a semi-vowel or special character that behaves like a vowel) in the form of new_accent. See test cases for example use.

  :param scheme: 
  :param text: 
  :param old_accent: 
  :param new_accent: 
  :param drop_at_first_syllable: Should text like "ॗसैषा᳘" be produced?
  :param retain_old_accent: 
  :return: 
  """
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
      if not retain_old_accent:
        out_letters.append(letter[:-1])
      else:
        out_letters.append(letter)
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
  text = add_accent_to_previous_syllable(scheme=scheme, text=text, new_accent=new_accent, old_accent=old_accent)
  return text


def add_accent_to_end(scheme, text, accent="᳟"):
  letters = "".join(scheme.get_letters())
  text = regex.sub(f"([{letters}])([^{letters}]+)$", f"\\1{accent}\\2", text)
  return text


def set_diirgha_svaritas(scheme, text, accent="᳚"):
  vowel_string = "".join(scheme.long_vowels + scheme.long_vowel_marks + list(scheme["yogavaahas"].values()))
  text = regex.sub(f"(?<=[{vowel_string}]+)॑", accent, text)
  return text


def strip_accents(text):
  return regex.sub(ACCENTS_PATTERN, "", text)


def to_US_accents(text, scheme=None, UDATTA = "꣡", SVARITA_NEW = "᳕", pauses=r"[।॥\n,;]+", skip_pattern=r"\+\+\+\(.+?\)\+\+\+"):
  """Given text like  
  ध्रु॒वो॑ऽसि ।  
  ध्रु॒वो॒॑ऽहँ स॑जा॒तेषु॑ भूयास॒न्  
  धीर॒श् चेत्ता॑ वसु॒वित्। 
  produce:
  ध्रुवो᳕ऽसि ।  
  ध्रुवो꣡ऽहँ꣡ सजाते꣡षु भूयासन्  
  धी꣡रश् चे꣡त्ता वसुवि꣡त्। 
  """
  # symbol definitions
  SANNATARA = "॒"
  SVARITA = "॑"
  if not any(x in text for x in [SVARITA, SANNATARA]):
    # Avoid inserting udattas from the beginning on an invalid (already converted input)
    return text
  if scheme == None:
    from indic_transliteration import sanscript
    scheme = sanscript.SCHEMES[sanscript.DEVANAGARI]

  PAUSES_PATTERN = regex.compile(pauses)
  SKIP_PATTERN = regex.compile(skip_pattern)

  # Split the text into a list of syllables and other elements.
  letters = scheme.split_vyanjanas_and_svaras(text, skip_pattern=skip_pattern)
  # Example output here - ['स्', "ओ", "+++(=tick)+++", 'ऽ', 'ग्', "न्", "इ॒", "म्", "ए॑", "व्", "अ"]

  out_letters = list(letters)


  # mark any syllable starting from a pause (or the beginning of out_text) as udAtta, until a sannatara or svarita
  for index, letter in enumerate(out_letters):
    if PAUSES_PATTERN.fullmatch(letter) or index == 0:
      mark_udAtta = True
    if mark_udAtta:
      # Scan forwards and mark succeeding syllables with Udatta.
      curr_fwd_index = scheme.get_adjacent_syllable_index(index-1, out_letters, +1, pauses_pattern=PAUSES_PATTERN)
      while mark_udAtta and curr_fwd_index is not None:
        syllable_to_check = out_letters[curr_fwd_index]
        # Stop if a barrier (a svarita or a pause) is reached.
        if any(x in syllable_to_check for x in [SVARITA_NEW, SVARITA, SANNATARA]):
          mark_udAtta = False
          break
        # Add Udatta if not already accented.
        if UDATTA not in out_letters[curr_fwd_index]:
          out_letters[curr_fwd_index] += UDATTA
        curr_fwd_index = scheme.get_adjacent_syllable_index(curr_fwd_index, out_letters, +1,
                                                            pauses_pattern=PAUSES_PATTERN)

  # --- PASS 1: Handle dependent Svarita (Rule 2) ---
  # If a syllable has a svarita and the predecessessor has a sannatara, remove both accents and add a svarita_new to the current syllable.
  # This rule (e.g., ध्रु॒वो॑ -> ध्रुवो᳕) is a specific substitution that takes precedence.
  for index, letter in enumerate(out_letters):
    # If a syllable has a svarita...
    if SVARITA in letter and not SANNATARA in letter:
      # ...and the predecessor has a sannatara...
      prev_index = scheme.get_adjacent_syllable_index(index, out_letters, -1, pauses_pattern=PAUSES_PATTERN)
      if prev_index is not None and SANNATARA in out_letters[prev_index]:
        # ... add a svarita_new to the current syllable.
        out_letters[index] += SVARITA_NEW

  for index, letter in enumerate(out_letters):
    is_kampa = SVARITA in letter and SANNATARA in letter  # Rule 1

    # If a syllable has both sannatara and svarita signs (like वो॒॑), replace it's svarita with udAtta, and temporarily keep the sannatara in itself. 
    if is_kampa:
      out_letters[index] = letter + UDATTA
      # Kampa rule: also remove the predecessor's sannatara.
      prev_index = scheme.get_adjacent_syllable_index(index, out_letters, -1, pauses_pattern=PAUSES_PATTERN)
      if prev_index is not None and SANNATARA in out_letters[prev_index]:
        out_letters[index] = out_letters[index].replace(SVARITA, "")

  # If a syllable has svarita, mark all preceeding syllables until a sannatara or svarita_new accent or a pause is reached with udAtta; at which point remove any preceding sannatara. 
  for index, letter in enumerate(out_letters):
    # --- Backward "painting" from a Svarita ---
    if not SVARITA in letter:
      continue
    # Remove the source accent(s) from the syllable.
    # For Kampa, also add an Udatta to the syllable itself.

    # Scan backwards and mark preceding syllables with Udatta.
    curr_back_index = scheme.get_adjacent_syllable_index(index, out_letters, -1, pauses_pattern=PAUSES_PATTERN)
    while curr_back_index is not None:
      syllable_to_check = out_letters[curr_back_index]
      if any(x in syllable_to_check for x in [SVARITA, SVARITA_NEW, SANNATARA]):
        # If the barrier is a sannatara, remove it and stop.
        break

      # Add Udatta if not already accented.
      if UDATTA not in out_letters[curr_back_index]:
        out_letters[curr_back_index] += UDATTA
      curr_back_index = scheme.get_adjacent_syllable_index(curr_back_index, out_letters, -1,
                                                           pauses_pattern=PAUSES_PATTERN)


  # If a syllable has sannatara, mark all succeeding syllables with udAtta until a svarita is reached or a pause is reached. Remove the triggering sannatara. After this is done for all syllables, there should be no sannatara left.
  for index, letter in enumerate(out_letters):

    # --- Forward "painting" from a Sannatara ---
    # This applies to simple sannatara only. Kampa's effect is handled above.
    if SANNATARA in letter:
      # Remove the triggering sannatara.
      out_letters[index] = letter.replace(SANNATARA, "")

      # Scan forwards and mark succeeding syllables with Udatta.
      curr_fwd_index = scheme.get_adjacent_syllable_index(index, out_letters, +1, pauses_pattern=PAUSES_PATTERN)
      while curr_fwd_index is not None:
        syllable_to_check = out_letters[curr_fwd_index]
        if SVARITA in syllable_to_check:
          break
        # Stop if a barrier (a svarita or a pause) is reached.
        if any(x in syllable_to_check for x in [SVARITA_NEW, SVARITA, SANNATARA]):
          break
        # Add Udatta if not already accented.
        if UDATTA not in out_letters[curr_fwd_index]:
          out_letters[curr_fwd_index] += UDATTA
        curr_fwd_index = scheme.get_adjacent_syllable_index(curr_fwd_index, out_letters, +1,
                                                            pauses_pattern=PAUSES_PATTERN)

  text = scheme.join_strings(out_letters)
  text = text.replace(SVARITA, "").replace(SANNATARA, "")
  return text
