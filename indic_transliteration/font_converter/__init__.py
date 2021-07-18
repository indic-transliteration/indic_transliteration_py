import logging


def is_ascii(word):
    # we've a mix of english and devanagari characters, decide which word to
    # convert based on the weight of english characters in the word :)
    # default threshold 0.7 means we consider a word to be english of 70% chars
    # are in ascii range 0-128.
    count_ascii = sum([1 if ord(c) < 128 else 0 for c in word])
    return count_ascii > 0.7 * len(word)


class Converter(object):

  # TODO : Handle svaras. https://github.com/sanskrit-coders/indic_transliteration_py/issues/38
  def _replace_line(self, line):
    if line.strip() == "":
        return line
    words = line.split(' ')
    line = ' '.join(self.convert(w) if not is_ascii(w) else w for w in words)
    return line.strip() + "  \n" # For markdown

  def convert(self, text):
    pass

  def convert_mixed(self, input_file, out_file):
    with open(input_file, 'r', encoding='utf-8') as f:
      with open(out_file, 'w', encoding='utf-8') as of:
        for line in f.readlines():
          outline = self._replace_line(line=line)
          logging.debug(outline)
          of.write(outline)
