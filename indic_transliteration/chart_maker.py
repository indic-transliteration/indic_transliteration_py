from indic_transliteration import sanscript

def get_script_map(scripts, base_script=sanscript.DEVANAGARI):
  base = sanscript.SCHEMES[base_script]
  base_letters = []
  base_letters.extend(base["vowels"].values())
  base_letters.extend(base["consonants"].values())
  base_letters.extend(base["extra_consonants"].values())
  vowel_marks = [""] + list(base["vowel_marks"].values()) + list(base["yogavaahas"].values()) + list(base["virama"].values())
  base_letters.extend(base["symbols"].values())
  for index, consonant in enumerate(list(base["consonants"].values())):
    letter = consonant + base["virama"]["्"] + base["consonants"]["क"] + vowel_marks[index % len(vowel_marks)]
    base_letters.append(letter)

  for index, accent in enumerate(list(base["accents"].values())):
    base_letters.append(base["consonants"]["क"] + vowel_marks[index % len(vowel_marks)] + accent)


  script_map = []
  for base_letter in base_letters:
    row = [base_letter]
    for script in scripts:
      row.append(sanscript.transliterate(base_letter, _from=base_script, _to=script))
    script_map.append(row)
  return script_map


def dump_script_map(dest_path, scripts, base_script=sanscript.DEVANAGARI, row_break=" # ", col_break=","):
  script_map = get_script_map(scripts=scripts, base_script=base_script)
  text = row_break.join([col_break.join(x) for x in script_map])
  from doc_curation.md.file import MdFile
  md_file = MdFile(file_path=dest_path)
  md_file.dump_to_file(metadata={"title": f"Chart of {len(scripts) + 1}"}, content=text, dry_run=False)


if __name__ == '__main__':
  dump_script_map(dest_path="/home/vvasuki/gitland/sanskrit/raw_etexts/mixed/vv_ebook_pub/experiment/de-iso-kn-ml-br.md", scripts=[sanscript.ISO, sanscript.KANNADA, sanscript.MALAYALAM, "brahmi"])