import regex

ACCENTS_PATTERN = r"[\u1CD0-\u1CE8\u1CF9\u1CFA\uA8E0-\uA8F1\u0951-\u0954\u0957]"  # included  ॗ , which is used as svara for weber's shatapatha


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


def detect_fake_US_accents(text, max_udaatta_seq=5):
  """Detect suspicious runs of consecutive UDATTA (᳓) marks in US-accented text.

  Genuine Vedic US-accented text does not normally have long unbroken runs of
  udatta-marked syllables.  Such runs usually indicate that a text was
  mechanically accented (for example, every syllable was marked with ᳓).

  Only consecutive udatta-marked syllables count.  Unaccented syllables,
  consonants, and spaces do not break a run; a dependent svarita (᳙) or a
  pause (danda, newline, comma or semicolon) does.

  :param text: text to inspect
  :param max_udaatta_seq: maximum number of udatta marks allowed before a run
    is considered fake
  :return: list of suspicious runs (empty list means no fake accents detected)
  """
  if "᳓" not in text:
    return []
  # Ignore annotations such as +++(...)+++; they may contain arbitrary accents.
  text = regex.sub(r"\+\+\+.*?\+\+\+", "", text, flags=regex.S)
  from indic_transliteration import sanscript
  scheme = sanscript.SCHEMES[sanscript.DEVANAGARI]
  vowels = set(scheme["vowels"].values())
  letters = scheme.split_vyanjanas_and_svaras(text)
  runs = []
  current = []
  for letter in letters:
    if letter and letter[0] in vowels:
      if "᳓" in letter:
        current.append(letter)
      else:
        if len(current) > max_udaatta_seq:
          runs.append("".join(current))
        current = []
    elif letter in ("।", "॥", ",", ";", "\n"):
      if len(current) > max_udaatta_seq:
        runs.append("".join(current))
      current = []
  if len(current) > max_udaatta_seq:
    runs.append("".join(current))
  return runs


def _decode_kampa(out_letters, scheme, pauses_pattern, skip_pattern, sannatara, svarita, svarita_new, udatta, av_svarita):
  """Decode syllable-attached Vedic kampa (१/३) while keeping true pluta ३ intact.

  Promotes kampa-bearing syllables to ``svarita_new``, removes kampa digit tokens,
  and returns ``(rebuilt_letters, kampa_anchor_indices)`` so Pass 4B paints subsequent udattas.
  """
  numerals = []
  try:
    numerals = scheme.get_numerals()
  except (KeyError, AttributeError):
    pass
  num_1 = numerals[1] if len(numerals) > 1 else "१"
  num_3 = numerals[3] if len(numerals) > 3 else "३"
  kampa_digits = {num_1, num_3}
  all_digits = set(numerals) | set("0123456789")
  accents_only = {svarita, sannatara, av_svarita, svarita_new, udatta}
  yogavaahas = set(scheme.get("yogavaahas", {}).values())
  accents_and_yogavaahas = accents_only | yogavaahas

  remove_indices = set()
  orig_anchors = set()
  for idx, tok in enumerate(out_letters):
    if not tok or skip_pattern.fullmatch(tok) or tok[0] not in kampa_digits:
      continue
    if any(ch not in accents_and_yogavaahas for ch in tok[1:]):
      continue
    if idx + 1 < len(out_letters) and out_letters[idx + 1] and out_letters[idx + 1][0] in all_digits:
      continue
    prev_syl = scheme.get_adjacent_syllable_index(idx, out_letters, -1, pauses_pattern=pauses_pattern)
    if prev_syl != idx - 1 or skip_pattern.fullmatch(out_letters[prev_syl]):
      continue
    next_syl = scheme.get_adjacent_syllable_index(idx, out_letters, +1, pauses_pattern=pauses_pattern)
    has_kampa_marks = sannatara in tok or svarita in tok
    if tok[0] != num_1 and not has_kampa_marks:
      # Bare pluta ३ marks kampa only when preceded by SVARITA and followed by an unmarked/non-sannatara syllable.
      is_kampa = (
        svarita in out_letters[prev_syl]
        and next_syl is not None
        and not skip_pattern.fullmatch(out_letters[next_syl])
        and sannatara not in out_letters[next_syl]
      )
      if not is_kampa:
        continue

    trailing_yogavaahas = "".join(ch for ch in tok[1:] if ch in yogavaahas)
    out_letters[prev_syl] = (
      out_letters[prev_syl]
      .replace(sannatara, "")
      .replace(svarita, "")
      .replace(av_svarita, "")
    )
    for yv in trailing_yogavaahas:
      if yv not in out_letters[prev_syl]:
        out_letters[prev_syl] += yv
    if svarita_new not in out_letters[prev_syl]:
      out_letters[prev_syl] += svarita_new
    if next_syl is not None and not skip_pattern.fullmatch(out_letters[next_syl]):
      nxt_tok = out_letters[next_syl]
      if svarita in nxt_tok and sannatara not in nxt_tok and av_svarita not in nxt_tok and svarita_new not in nxt_tok:
        out_letters[next_syl] = nxt_tok.replace(svarita, "")
    remove_indices.add(idx)
    orig_anchors.add(prev_syl)

  if not remove_indices:
    return out_letters, set()

  rebuilt = []
  kampa_anchors = set()
  for idx, tok in enumerate(out_letters):
    if idx in remove_indices:
      continue
    if idx in orig_anchors:
      kampa_anchors.add(len(rebuilt))
    rebuilt.append(tok)
  return rebuilt, kampa_anchors


def _decode_av_svarita(out_letters, scheme, pauses_pattern, skip_pattern, sannatara, svarita, svarita_new, av_svarita):
  """Convert Atharvavedic independent svarita marks (᳡) to ``svarita_new`` and clear post-᳡ anudatta ``॑`` dips."""
  av_indices = [
    idx for idx, tok in enumerate(out_letters)
    if av_svarita in tok and tok[0] not in (svarita, sannatara, av_svarita) and not skip_pattern.fullmatch(tok)
  ]
  for idx in av_indices:
    nxt = scheme.get_adjacent_syllable_index(idx, out_letters, +1, pauses_pattern=pauses_pattern)
    if nxt is not None and not skip_pattern.fullmatch(out_letters[nxt]):
      nxt_tok = out_letters[nxt]
      if svarita in nxt_tok and sannatara not in nxt_tok and av_svarita not in nxt_tok and svarita_new not in nxt_tok:
        out_letters[nxt] = nxt_tok.replace(svarita, "")
  for idx in av_indices:
    tok = out_letters[idx].replace(av_svarita, "").replace(svarita, "").replace(sannatara, "")
    if svarita_new not in tok:
      tok += svarita_new
    out_letters[idx] = tok


def to_US_accents(text, scheme=None, UDATTA = "᳓", SVARITA_NEW = "᳙", pauses=r"[।॥\n,;]+", skip_pattern=r"\+\+\+\((.+?)\)\+\+\+", SANNATARA_NEW="", DEP_SVARITA_NEW=""):
  """Given text like  
  ध्रु॒वो॑ऽसि ।  
  ध्रु॒वो॒॑ऽहँ स॑जा॒तेषु॑ भूयास॒न्  
  धीर॒श् चेत्ता॑ वसु॒वित्। 
  produce something like:
  ध्रुवो᳕ऽसि ।  
  ध्रुवो꣡ऽहँ꣡ सजाते꣡षु भूयासन्  
  धी꣡रश् चे꣡त्ता वसुवि꣡त्। 
  """
  # symbol definitions
  SANNATARA = "॒"
  SVARITA = "॑"
  AV_SVARITA = "᳡"
  if not any(x in text for x in [SVARITA, SANNATARA, "᳚", "᳛", AV_SVARITA]):
    # Avoid inserting udattas from the beginning on an invalid (already converted input)
    return text
  if any(x in text for x in [SVARITA_NEW, UDATTA]):
    return text
  text = regex.sub("[᳖᳚᳛]", SVARITA, text)
  if scheme == None:
    from indic_transliteration import sanscript
    scheme = sanscript.SCHEMES[sanscript.DEVANAGARI]

  PAUSES_PATTERN = regex.compile(pauses)
  SKIP_PATTERN = regex.compile(skip_pattern)

  # Split the text into a list of syllables and other elements.
  skip_pattern_noncapture = regex.sub(r"(?<=^|[^\\])\(", "(?:", skip_pattern)
  letters = scheme.split_vyanjanas_and_svaras(text, skip_pattern=skip_pattern_noncapture)
  # Example output here - ['स्', "ओ", "+++(=tick)+++", 'ऽ', 'ग्', "न्", "इ॒", "म्", "ए॑", "व्", "अ"]

  out_letters = list(letters)
  # Unattached orphan accent marks (e.g. leading "॑" with no base syllable) carry no valid accent pattern.
  source_marks = (SVARITA, SANNATARA, AV_SVARITA)
  if not any(
    tok and (
      (SKIP_PATTERN.fullmatch(tok) and any(m in tok for m in source_marks))
      or (not SKIP_PATTERN.fullmatch(tok) and tok[0] not in source_marks and any(m in tok for m in source_marks))
    )
    for tok in out_letters
  ):
    return text

  out_letters, kampa_anchors = _decode_kampa(
    out_letters, scheme, PAUSES_PATTERN, SKIP_PATTERN, SANNATARA, SVARITA, SVARITA_NEW, UDATTA, AV_SVARITA
  )
  _decode_av_svarita(
    out_letters, scheme, PAUSES_PATTERN, SKIP_PATTERN, SANNATARA, SVARITA, SVARITA_NEW, AV_SVARITA
  )

  # mark any syllable starting from a pause (or the beginning of out_text) as udAtta, until a sannatara or svarita
  for index, letter in enumerate(out_letters):
    if index == 0 or PAUSES_PATTERN.fullmatch(out_letters[index-1]):
      first_vowel_index = scheme.get_adjacent_syllable_index(index-1, out_letters, +1, pauses_pattern=PAUSES_PATTERN)
      if first_vowel_index is not None and any(x in out_letters[first_vowel_index] for x in [SVARITA, SVARITA_NEW]):
        if SANNATARA not in out_letters[first_vowel_index] and SVARITA_NEW not in out_letters[first_vowel_index]:
          # Phrase-initial svarita (not kampa) has no preceding vowel, so it is always non-dependent svarita (᳙).
          out_letters[first_vowel_index] += SVARITA_NEW
        mark_udAtta = False
      else:
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
    # Deal with accented text like दु॒श्चरि॑तं॒ in SKIP_PATTERN
    if SKIP_PATTERN.fullmatch(letter):
      continue

    # If a syllable has a non-kampa svarita and its predecessor is NOT an udAtta
    # (no predecessor, predecessor has sannatara, or predecessor is itself a non-kampa svarita),
    # mark it as non-dependent svarita (SVARITA_NEW).
    if (
      SVARITA in letter
      and letter[0] not in (SVARITA, SANNATARA, AV_SVARITA)
      and SANNATARA not in letter
      and SVARITA_NEW not in letter
    ):
      prev_index = scheme.get_adjacent_syllable_index(index, out_letters, -1, pauses_pattern=PAUSES_PATTERN)
      if (
        prev_index is None
        or SANNATARA in out_letters[prev_index]
        or (SVARITA in out_letters[prev_index] and SANNATARA not in out_letters[prev_index])
      ):
        out_letters[index] += SVARITA_NEW

  pass
  for index, letter in enumerate(out_letters):
    is_kampa = SVARITA in letter and SANNATARA in letter  # Rule 1
    
    # Deal with accented text like दु॒श्चरि॑तं॒ in SKIP_PATTERN
    if SKIP_PATTERN.fullmatch(letter):
      continue

    # If a syllable has both sannatara and svarita signs (like वो॒॑), replace it's svarita with udAtta, and temporarily keep the sannatara in itself. 
    if is_kampa:
      if UDATTA not in out_letters[index]:
        out_letters[index] += UDATTA
      # Kampa rule: also remove the predecessor's sannatara.
      prev_index = scheme.get_adjacent_syllable_index(index, out_letters, -1, pauses_pattern=PAUSES_PATTERN)
      if prev_index is not None and SANNATARA in out_letters[prev_index]:
        out_letters[index] = out_letters[index].replace(SVARITA, "")

  pass
  # If a syllable has svarita, mark all preceeding syllables until a sannatara or svarita_new accent or a pause is reached with udAtta; at which point remove any preceding sannatara. 
  for index, letter in enumerate(out_letters):
    # Deal with accented text like दु॒श्चरि॑तं॒ in SKIP_PATTERN
    if SKIP_PATTERN.fullmatch(letter):
      continue

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


  pass
  virama = scheme["virama"].get("्", "")
  ya_halant = scheme["consonants"].get("य", "") + virama if virama and "य" in scheme["consonants"] else ""
  da_halant = scheme["consonants"].get("द", "") + virama if virama and "द" in scheme["consonants"] else ""
  ra_halant = scheme["consonants"].get("र", "") + virama if virama and "र" in scheme["consonants"] else ""
  sa_halant = scheme["consonants"].get("स", "") + virama if virama and "स" in scheme["consonants"] else ""
  ka_halant = scheme["consonants"].get("क", "") + virama if virama and "क" in scheme["consonants"] else ""
  ma_halant = scheme["consonants"].get("म", "") + virama if virama and "म" in scheme["consonants"] else ""
  a_vowel = scheme["vowels"].get("अ", "")
  aa_vowel = scheme["vowels"].get("आ", "")
  ai_vowel = scheme["vowels"].get("ऐ", "")
  o_vowel = scheme["vowels"].get("ओ", "")
  yo_ye_vowels = {v for k in ("ओ", "ए") if (v := scheme["vowels"].get(k))}
  non_ru_vowels = {v for k in ("अ", "आ", "ऊ", "औ") if (v := scheme["vowels"].get(k))}
  avagraha = scheme.get("symbols", {}).get("ऽ", "ऽ")
  vowels_set = set(scheme["vowels"].values())
  yogavaahas_set = set(scheme.get("yogavaahas", {}).values())
  word_chars_set = vowels_set | yogavaahas_set | {"-"}
  pada_end_nasals = tuple(
    scheme["consonants"].get(c, "") + virama + candra
    for c in ("ल", "व", "य")
    if virama and scheme["consonants"].get(c) and (candra := scheme.get("yogavaahas", {}).get("ँ"))
  )

  def _paint_forward_udatta(start_index):
    curr_fwd_index = scheme.get_adjacent_syllable_index(start_index, out_letters, +1, pauses_pattern=PAUSES_PATTERN)
    while curr_fwd_index is not None:
      syllable_to_check = out_letters[curr_fwd_index]
      # Stop if a barrier (a svarita, sannatara, or pause) is reached.
      if any(x in syllable_to_check for x in [SVARITA_NEW, SVARITA, SANNATARA]):
        break
      # Add Udatta if not already accented.
      if UDATTA not in out_letters[curr_fwd_index]:
        out_letters[curr_fwd_index] += UDATTA
      curr_fwd_index = scheme.get_adjacent_syllable_index(curr_fwd_index, out_letters, +1,
                                                          pauses_pattern=PAUSES_PATTERN)

  def _is_unaccented_enclitic_after_avagraha(av_index):
    # AnvAdesha enclitic forms ऽस्य / ऽस्मै (PAnini 2.4.32) immediately after यो॑/ये॑ carry no udAtta.
    k = av_index + 1
    while k < len(out_letters) and out_letters[k].isspace():
      k += 1
    if k + 2 >= len(out_letters) or not sa_halant or out_letters[k] != sa_halant:
      return False
    c2, v = out_letters[k + 1], out_letters[k + 2]
    is_sya = ya_halant and a_vowel and c2 == ya_halant and v == a_vowel
    is_smai = ma_halant and ai_vowel and c2 == ma_halant and v == ai_vowel
    if not (is_sya or is_smai):
      return False
    nxt = k + 3
    return nxt >= len(out_letters) or out_letters[nxt].isspace() or bool(PAUSES_PATTERN.fullmatch(out_letters[nxt])) or bool(SKIP_PATTERN.fullmatch(out_letters[nxt]))

  def _succeeding_word_has_udatta(av_index):
    word_syl_indices = []
    seen_word_char = False
    for k in range(av_index + 1, len(out_letters)):
      tok = out_letters[k]
      if not tok or PAUSES_PATTERN.fullmatch(tok) or SKIP_PATTERN.fullmatch(tok):
        break
      if tok.isspace():
        if not seen_word_char:
          continue
        break
      if tok == avagraha:
        # A second avagraha after an accented/sannatara syllable starts a new pada (e.g. ये॑ऽमुतो॒ऽर्वाञ्च॑म्),
        # whereas unaccented internal avagraha in aluk-samAsa (e.g. यो॑ऽरण्येऽनुवा॒क्यो॑) continues the compound.
        if word_syl_indices and any(x in out_letters[word_syl_indices[-1]] for x in (SANNATARA, UDATTA, SVARITA_NEW, SVARITA)):
          break
        seen_word_char = True
        continue
      if tok[0] in vowels_set:
        seen_word_char = True
        word_syl_indices.append(k)
        # Word-final anunAsika sandhi (-ल्ँ / -व्ँ / -य्ँ) marks the end of the pada even when unspaced.
        if pada_end_nasals and any(p in tok for p in pada_end_nasals):
          break
      elif (virama and tok.endswith(virama)) or tok[0] in word_chars_set:
        seen_word_char = True
        # Visarga repha after ए/ओ (-एर्/-ओर् + consonant, e.g. यो॑ऽग्नेर्दे॒वता॑याः) only occurs at a pada boundary.
        if ra_halant and tok == ra_halant and word_syl_indices and word_syl_indices[-1] == k - 1 and out_letters[k - 1][0] in yo_ye_vowels:
          break
      else:
        break
    if not word_syl_indices:
      return False
    if any(UDATTA in out_letters[k] or SVARITA_NEW in out_letters[k] for k in word_syl_indices):
      return True
    # Non-final sannatara rises to an udAtta within this same word in the forward pass.
    return any(SANNATARA in out_letters[k] for k in word_syl_indices[:-1])

  def _find_yo_ye_vowel_before_avagraha(av_index):
    # Relative pronoun यो॑/ये॑ (यः/ये, standalone or after external -र्/-द् sandhi) + ऽ
    # carries an independent accent (abhinihita) and elides a following sannatara अ॒ without leaving ॒ behind.
    if out_letters[av_index] != avagraha or not ya_halant or not yo_ye_vowels:
      return None
    vi = av_index - 1
    while vi >= 1 and (out_letters[vi].isspace() or SKIP_PATTERN.fullmatch(out_letters[vi])):
      vi -= 1
    if (
      vi < 1
      or SVARITA not in out_letters[vi]
      or SANNATARA in out_letters[vi]
      or out_letters[vi][0] not in yo_ye_vowels
      or out_letters[vi - 1] != ya_halant
    ):
      return None
    if vi - 1 == 0:
      return vi
    prev_tok = out_letters[vi - 2]
    if not prev_tok or prev_tok == avagraha:
      return None
    # Standalone यो॑/ये॑ after whitespace, pause/punctuation, or word-final yogavAha (e.g. ताय्ँ॒यो॑ऽ).
    if prev_tok[0] not in vowels_set and not (virama and prev_tok.endswith(virama)):
      return vi
    if prev_tok[0] in vowels_set and any(y in prev_tok for y in yogavaahas_set):
      return vi
    # External sandhi before यः/ये without space: -त्/-द् + यः/ये -> -द्यो॑ऽ/-द्ये॑ऽ (e.g. भूया॒द्यो॑ऽ, यद्ब्रू॒याद्यो॑ऽ),
    # or non-अ/आ/ऊ/औ visarga + यः -> -र्यो॑ऽ (e.g. भूयासु॒र्यो॑ऽ, पाशै॒र्यो॑ऽ; excludes आचा॒र्यो॑ऽ, का॒र्यो॑ऽ, सू॒र्यो॑ऽ, सौ॒र्यो॑ऽ).
    if da_halant and prev_tok == da_halant and vi >= 3 and out_letters[vi - 3][0] in vowels_set:
      if SVARITA_NEW in out_letters[vi]:
        return vi
      if aa_vowel and ya_halant and vi >= 4 and out_letters[vi - 3][0] == aa_vowel and out_letters[vi - 4] == ya_halant:
        return vi
    if SVARITA_NEW in out_letters[vi] and vi >= 3 and out_letters[vi - 3][0] in vowels_set:
      if ra_halant and prev_tok == ra_halant and out_letters[vi][0] == o_vowel and out_letters[vi - 3][0] not in non_ru_vowels:
        return vi
    return None

  def _find_so_ko_vowel_before_avagraha(av_index):
    # Standalone orthotone pronouns सो॑ऽ / को॑ऽ (सः/कः + अ-) carry non-dependent abhinihita svarita even after an udAtta word.
    if out_letters[av_index] != avagraha or not o_vowel:
      return None
    vi = av_index - 1
    while vi >= 1 and (out_letters[vi].isspace() or SKIP_PATTERN.fullmatch(out_letters[vi])):
      vi -= 1
    if (
      vi < 1
      or SVARITA not in out_letters[vi]
      or SANNATARA in out_letters[vi]
      or out_letters[vi][0] != o_vowel
      or out_letters[vi - 1] not in {c for c in (sa_halant, ka_halant) if c}
    ):
      return None
    if vi - 1 == 0:
      return vi
    prev_tok = out_letters[vi - 2]
    if prev_tok and prev_tok != avagraha and prev_tok[0] not in vowels_set and not (virama and prev_tok.endswith(virama)):
      return vi
    return None

  # --- PASS 4A: Handle pre-avagraha abhinihita svarita (यो॑ऽ / ये॑ऽ, सो॑ऽ / को॑ऽ) BEFORE SANNATARA barriers are removed ---
  for index, letter in enumerate(out_letters):
    if SKIP_PATTERN.fullmatch(letter):
      continue
    yo_ye_vi = _find_yo_ye_vowel_before_avagraha(index)
    if yo_ye_vi is not None:
      if SVARITA_NEW not in out_letters[yo_ye_vi]:
        out_letters[yo_ye_vi] = out_letters[yo_ye_vi].replace(UDATTA, "") + SVARITA_NEW
      if not _succeeding_word_has_udatta(index) and not _is_unaccented_enclitic_after_avagraha(index):
        _paint_forward_udatta(index)
      continue
    so_ko_vi = _find_so_ko_vowel_before_avagraha(index)
    if so_ko_vi is not None and SVARITA_NEW not in out_letters[so_ko_vi]:
      out_letters[so_ko_vi] = out_letters[so_ko_vi].replace(UDATTA, "") + SVARITA_NEW

  # --- PASS 4B: Forward "painting" from a Sannatara ---
  # If a syllable has sannatara, mark all succeeding syllables with udAtta until a svarita, sannatara, or pause is reached. Remove the triggering sannatara. After this is done for all syllables, there should be no sannatara left.
  for index, letter in enumerate(out_letters):
    # Deal with accented text like दु॒श्चरि॑तं॒ in SKIP_PATTERN
    if SKIP_PATTERN.fullmatch(letter):
      continue

    # Trigger forward udatta painting on sannatara or decoded kampa anchor syllables.
    if SANNATARA in letter or index in kampa_anchors:
      if SANNATARA in letter:
        out_letters[index] = letter.replace(SANNATARA, "")
      _paint_forward_udatta(index)

  pass
  for index, letter in enumerate(out_letters):
    match = SKIP_PATTERN.match(letter)
    if match:
      replacement = to_US_accents(text=match.group(1), scheme=scheme, UDATTA=UDATTA, SVARITA_NEW=SVARITA_NEW, pauses=pauses, skip_pattern=skip_pattern)
      out_letters[index] = letter.replace(match.group(1), replacement)


  text = scheme.join_strings(out_letters)
  text = text.replace(SVARITA, DEP_SVARITA_NEW).replace(SANNATARA, SANNATARA_NEW)
  return text


def add_dependent_accents(text, scheme=None, UDATTA = "᳓", SVARITA = "᳙", pauses=r"[।॥\n,;]+", skip_pattern=r"\+\+\+\((.+?)\)\+\+\+", SANNATARA="॒", DEP_SVARITA="᳜", UDATTA_NEW=None):
  """Inverse of to_US_accents: convert udAtta(᳓)-svarita(᳙) accented text into the traditional "dependent accented" notation, where only the non-default accents are marked.

  - udAtta syllables are left as they are (UDATTA_NEW = UDATTA by default); pass UDATTA_NEW="" to leave them unmarked as in traditional Vedic printing.
  - An anudAtta syllable which rises to a following accented syllable (udAtta or svarita) is marked with a sannatara (SANNATARA = ॒) - eg: दर्शपूर्णमा॒सयो᳙स्सृ॒ष्टयो᳙र्
  - An anudAtta syllable which falls from a preceding udAtta is a dependent svarita, and is marked with DEP_SVARITA (᳜ by default; pass "॑" to get the classical Yajurveda print style) - eg: ग्रहो᳜, सो᳜.
  - Independent svaritas (already marked with SVARITA = ᳙ in the input) are left untouched - eg: न्यू᳙नया.

  So add_dependent_accents(text=to_US_accents(text=classically_accented_text), UDATTA_NEW="", DEP_SVARITA="॑") round-trips classical text.

  :param text: text accented with UDATTA (᳓) and SVARITA (᳙) marks.
  :param scheme: scheme of the text; Devanagari by default.
  :param UDATTA: mark of an udAtta syllable in the input.
  :param SVARITA: mark of an (independent) svarita syllable in the input.
  :param pauses: pattern which separates accentual phrases; accents are never marked across it.
  :param skip_pattern: annotations like +++(...)+++ which should be accented separately.
  :param SANNATARA: mark to add to an anudAtta syllable rising to a following accent.
  :param DEP_SVARITA: mark to add to a dependent svarita syllable.
  :param UDATTA_NEW: mark to replace UDATTA with; UDATTA itself by default.
  :return:
  """
  if UDATTA_NEW is None:
    UDATTA_NEW = UDATTA
  if UDATTA not in text and SVARITA not in text:
    # Nothing to do for unaccented (or already dependent-accented) text.
    return text
  if any(x in text for x in [SANNATARA, DEP_SVARITA] if x):
    # Avoid adding dependent accents twice.
    return text
  if scheme == None:
    from indic_transliteration import sanscript
    scheme = sanscript.SCHEMES[sanscript.DEVANAGARI]

  PAUSES_PATTERN = regex.compile(pauses)
  SKIP_PATTERN = regex.compile(skip_pattern)

  # Split the text into a list of syllables and other elements.
  skip_pattern_noncapture = regex.sub(r"(?<=^|[^\\])\(", "(?:", skip_pattern)
  letters = scheme.split_vyanjanas_and_svaras(text, skip_pattern=skip_pattern_noncapture)
  out_letters = list(letters)

  udAtta_indices = set(index for index, letter in enumerate(letters) if UDATTA in letter)
  svarita_indices = set(index for index, letter in enumerate(letters) if SVARITA in letter)
  accented_indices = udAtta_indices | svarita_indices

  # udAtta marks are replaced by UDATTA_NEW (pass UDATTA_NEW="" to leave them unmarked, as in traditional printing).
  for index in udAtta_indices:
    out_letters[index] = out_letters[index].replace(UDATTA, UDATTA_NEW)

  # AnudAtta syllables get a dependent accent, which is determined by their neighbouring accents.
  vowels_set = set(scheme["vowels"].values())
  for index, letter in enumerate(letters):
    # Deal with accented text like दु॒श्चरि॑तं॒ in SKIP_PATTERN
    if SKIP_PATTERN.fullmatch(letter):
      continue
    # Only unaccented syllables (ie. anudAttas) need a dependent accent.
    if index in accented_indices or letter[0] not in vowels_set:
      continue

    next_index = scheme.get_adjacent_syllable_index(index, letters, +1, pauses_pattern=PAUSES_PATTERN)
    prev_index = scheme.get_adjacent_syllable_index(index, letters, -1, pauses_pattern=PAUSES_PATTERN)
    if next_index is not None and next_index in accented_indices:
      # The voice rises from this syllable to the following accent.
      out_letters[index] += SANNATARA
    elif prev_index is not None and prev_index in udAtta_indices:
      # The voice falls from the preceding udAtta - hence a dependent svarita.
      out_letters[index] += DEP_SVARITA

  # Accent the annotations like +++(...)+++ separately.
  for index, letter in enumerate(out_letters):
    match = SKIP_PATTERN.match(letter)
    if match:
      replacement = add_dependent_accents(text=match.group(1), scheme=scheme, UDATTA=UDATTA, SVARITA=SVARITA,
                                          pauses=pauses, skip_pattern=skip_pattern, SANNATARA=SANNATARA,
                                          DEP_SVARITA=DEP_SVARITA, UDATTA_NEW=UDATTA_NEW)
      out_letters[index] = letter.replace(match.group(1), replacement)

  text = scheme.join_strings(out_letters)
  return text

def fix_kAThaka_notation(text, UDATTA="᳓", SVARITA="᳙", skip_pattern=r"\+\+\+\((.+?)\)\+\+\+"):
  """Translate Kāṭhaka / Schroeder edition accent notation to our US accent notation.

  In Leopold von Schroeder's edition of the Kāṭhaka Saṁhitā:
  - Udātta is marked by a vertical stroke above the syllable: ॑ (U+0951).
  - Independent svarita is marked by a curve/hook: ᳙ (U+1CD9), ᳗ (U+1CD7), ᳖ (U+1CD6), ᳚ (U+1CDA).
  - Anudātta and secondary (dependent) svarita are left unmarked.

  This function translates these marks to our US notation (losslessly):
  - ॑ (U+0951) -> UDATTA (default: ᳓ U+1CD3)
  - ᳙, ᳗, ᳖, ᳚ -> SVARITA (default: ᳙ U+1CD9)

  :param text: input text in Kāṭhaka / Schroeder notation
  :param UDATTA: replacement for udātta (default: "᳓")
  :param SVARITA: replacement for independent svarita (default: "᳙")
  :param skip_pattern: pattern for annotations to be skipped or processed separately
  :return: text in our US accent notation
  """
  def _replace(t):
    t = regex.sub(r"[᳖᳗᳙᳚]", SVARITA, t)
    t = t.replace("॑", UDATTA)
    return t

  if skip_pattern:
    SKIP_PATTERN = regex.compile(skip_pattern, flags=regex.DOTALL)
    parts = []
    last_end = 0
    for match in SKIP_PATTERN.finditer(text):
      parts.append(_replace(text[last_end:match.start()]))
      inner_replaced = fix_kAThaka_notation(match.group(1), UDATTA=UDATTA, SVARITA=SVARITA, skip_pattern=skip_pattern)
      parts.append(match.group(0).replace(match.group(1), inner_replaced))
      last_end = match.end()
    parts.append(_replace(text[last_end:]))
    return "".join(parts)
  else:
    return _replace(text)


def from_US_to_kAThaka_notation(text, UDATTA="॑", SVARITA="᳙", skip_pattern=r"\+\+\+\((.+?)\)\+\+\+"):
  """Inverse of fix_kAThaka_notation: translate US accent notation back to Kāṭhaka / Schroeder notation.

  - UDATTA mark (᳓ U+1CD3) -> UDATTA (default: ॑ U+0951)
  - SVARITA mark (᳙ U+1CD9) -> SVARITA (default: ᳙ U+1CD9)
  """
  def _replace(t):
    t = t.replace("᳓", UDATTA)
    t = t.replace("᳙", SVARITA)
    return t

  if skip_pattern:
    SKIP_PATTERN = regex.compile(skip_pattern, flags=regex.DOTALL)
    parts = []
    last_end = 0
    for match in SKIP_PATTERN.finditer(text):
      parts.append(_replace(text[last_end:match.start()]))
      inner_replaced = from_US_to_kAThaka_notation(match.group(1), UDATTA=UDATTA, SVARITA=SVARITA, skip_pattern=skip_pattern)
      parts.append(match.group(0).replace(match.group(1), inner_replaced))
      last_end = match.end()
    parts.append(_replace(text[last_end:]))
    return "".join(parts)
  else:
    return _replace(text)
