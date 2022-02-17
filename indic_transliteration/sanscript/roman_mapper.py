import regex
from indic_transliteration.sanscript.schemes import roman


def _roman(data, scheme_map, **kw):
  """Transliterate `data` with the given `scheme_map`. This function is used
  when the source scheme is a Roman scheme.

  :param data: the data to transliterate
  :param scheme_map: a dict that maps between characters in the old scheme
                     and characters in the new scheme
  """

  vowels = scheme_map.vowels
  vowel_marks = scheme_map.vowel_marks
  virama = scheme_map.virama
  consonants = scheme_map.consonants
  non_marks_viraama = scheme_map.non_marks_viraama
  max_key_length_from_scheme = scheme_map.max_key_length_from_scheme
  to_roman = scheme_map.to_scheme.is_roman

  togglers = kw.pop('togglers', set())
  suspend_on = kw.pop('suspend_on', set())
  suspend_off = kw.pop('suspend_off', set())
  kw.pop('maybe_use_dravidian_variant', None)
  if kw:
    raise TypeError('Unexpected keyword argument %s' % list(kw.keys())[0])

  buf = []
  i = 0
  had_consonant = found = False
  len_data = len(data)
  append = buf.append

  # If true, don't transliterate. The toggle token is discarded.
  toggled = False
  # If true, don't transliterate. The suspend token is retained.
  # `suspended` overrides `toggled`.
  suspended = False

  while i <= len_data:
    # The longest token in the source scheme has length `max_key_length_from_scheme`. Iterate
    # over `data` while taking `max_key_length_from_scheme` characters at a time. If we don`t
    # find the character group in our scheme map, lop off a character and
    # try again.
    #
    # If we've finished reading through `data`, then `token` will be empty
    # and the loop below will be skipped.
    token = data[i:i + max_key_length_from_scheme]

    while token:
      if token in togglers:
        toggled = not toggled
        i += 2  # skip over the token
        found = True  # force the token to fill up again
        break

      if token in suspend_on:
        suspended = True
      elif token in suspend_off:
        suspended = False

      if toggled or suspended:
        token = token[:-1]
        continue

      # Catch the pattern CV, where C is a consonant and V is a vowel.
      # V should be rendered as a vowel mark, a.k.a. a "dependent"
      # vowel. But due to the nature of Brahmic scripts, 'a' is implicit
      # and has no vowel mark. If we see 'a', add nothing.
      if had_consonant and token in vowels:
        mark = vowel_marks.get(token, '')
        if mark:
          append(mark)
        elif to_roman:
          append(vowels[token])
        found = True

      # Catch any non_marks_viraama character, including consonants, punctuation,
      # and regular vowels. Due to the implicit 'a', we must explicitly
      # end any lingering consonants before we can handle the current
      # token.
      elif token in non_marks_viraama:
        if had_consonant:
          append(virama[''])
        append(non_marks_viraama[token])
        found = True

      if found:
        had_consonant = token in consonants
        i += len(token)
        break
      else:
        token = token[:-1]

    # We've exhausted the token; this must be some other character. Due to
    # the implicit 'a', we must explicitly end any lingering consonants
    # before we can handle the current token.
    if not found:
      if had_consonant:
        append(virama[''])
      if i < len_data:
        append(data[i])
        had_consonant = False
      i += 1

    found = False

  result = ''.join(buf)
  if not to_roman and len(scheme_map.accents) > 0:
    pattern = "([%s])([%s])" % ("".join(scheme_map.accents.values()), "".join(scheme_map.to_scheme['yogavaahas']))
    result = regex.sub(pattern, "\\2\\1", result)
  
  if scheme_map.from_scheme.name in roman.CAPITALIZABLE_SCHEME_IDS:
    result = scheme_map.to_scheme.fix_om(result)

  return result