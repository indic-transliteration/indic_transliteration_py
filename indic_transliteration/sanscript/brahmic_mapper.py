import regex

from indic_transliteration.sanscript.schemes import brahmic


def _brahmic(data, scheme_map, **kw):
  """Transliterate `data` with the given `scheme_map`. This function is used
  when the source scheme is a Brahmic scheme.

  :param data: the data to transliterate
  :param scheme_map: a dict that maps between characters in the old scheme
                     and characters in the new scheme
  """
  if scheme_map.from_scheme.name == brahmic.GURMUKHI:
    data = brahmic.GurmukhiScheme.replace_addak(text=data)
  elif scheme_map.from_scheme.name == brahmic.TAMIL_SUB:
    data = brahmic.TamilScheme.move_before_maatraa_subscripts(text=data)
  elif scheme_map.from_scheme.name == brahmic.TAMIL_SUP:
    data = brahmic.TamilScheme.move_before_maatraa_superscripts(text=data)
  vowel_marks = scheme_map.vowel_marks
  virama = scheme_map.virama
  consonants = scheme_map.consonants
  non_marks_viraama = scheme_map.non_marks_viraama
  to_roman = scheme_map.to_scheme.is_roman
  max_key_length_from_scheme = scheme_map.max_key_length_from_scheme

  if to_roman and len(scheme_map.accents) > 0:
    pattern = "([%s])([%s])" % ("".join(scheme_map.from_scheme['yogavaahas']), "".join(scheme_map.accents.keys()))
    data = regex.sub(pattern, "\\2\\1", data)

  buf = []
  i = 0
  to_roman_had_consonant = found = False
  append = buf.append
  # logging.debug(pprint.pformat(scheme_map.consonants))

  # We dont just translate each brAhmic character one after another in order to prefer concise transliterations when possible - for example ज्ञ -> jn in optitrans rather than j~n.
  while i <= len(data):
    # The longest token in the source scheme has length `max_key_length_from_scheme`. Iterate
    # over `data` while taking `max_key_length_from_scheme` characters at a time. If we don`t
    # find the character group in our scheme map, lop off a character and
    # try again.
    #
    # If we've finished reading through `data`, then `token` will be empty
    # and the loop below will be skipped.
    token = data[i:i + max_key_length_from_scheme]

    while token:
      if len(token) == 1:
        if token in vowel_marks:
          append(vowel_marks[token])
          found = True
        elif token in virama:
          append(virama[token])
          found = True
        else:
          if to_roman_had_consonant:
            append('a')
          append(non_marks_viraama.get(token, token))
          found = True
      else:
        if token in non_marks_viraama:
          if to_roman_had_consonant:
            append('a')
          append(non_marks_viraama.get(token))
          found = True

      if found:
        to_roman_had_consonant = to_roman and token in consonants
        i += len(token)
        break        
      else:
        token = token[:-1]

    # Continuing the outer while loop.
    # We've exhausted the token; this must be some other character. Due to
    # the implicit 'a', we must explicitly end any lingering consonants
    # before we can handle the current token.
    if not found:
      if to_roman_had_consonant:
        append(next(iter(virama.values())))
      if i < len(data):
        append(data[i])
        to_roman_had_consonant = False
      i += 1

    found = False

  if to_roman_had_consonant:
    append('a')
  return ''.join(buf)