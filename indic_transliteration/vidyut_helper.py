from vidyut.lipi import transliterate, Scheme


def dev(x):
  return transliterate(str(x), Scheme.Slp1, Scheme.Devanagari)


def slp(x):
  return transliterate(str(x), Scheme.Devanagari, Scheme.Slp1)
