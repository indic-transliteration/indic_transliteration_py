import codecs
import logging
import os
import aksharamukha.transliterate
import pandas
import tqdm
import regex

from indic_transliteration import tamil_tools


def transliterate_tamil(text, dest_script="DEVANAGARI", aksharamukha_pre_options=["TamilTranscribe"], aksharamukha_post_options=[]):
  source_script = "TAMIL"
  dest_script = dest_script.capitalize()
  text = regex.sub("ற", r"ऱ", text)
  text = regex.sub("ன", r"ऩ", text)
  # https://github.com/virtualvinodh/aksharamukha-python/issues/21
  text = aksharamukha.transliterate.process(src=source_script, tgt=dest_script, txt=text, nativize = True, pre_options = aksharamukha_pre_options, post_options = aksharamukha_post_options)
  text = text.replace("\u200c", "")
  # https://github.com/virtualvinodh/aksharamukha-python/issues/22
  text = regex.sub("म्([सव])", r"ं\1", text)
  
  # Mitigate consequences of ऩ ऱ insertions.
  text = tamil_tools.soften(text=text, pattern="(?<=[ऩ][ा-्]?)({})(?!्)")
  text = tamil_tools.soften(text=text, pattern="(?<=[ऱ][ा-ौ]?)({})(?!्)")
  # text = regex.sub("।", r".", text)
  return text


def convert_file(source_path, dest_path, source_script, dest_script, pre_options = [], post_options = []):
  logging.info("\nTransliterating (%s > %s) %s to %s", source_script, dest_script, source_path, dest_path)
  os.makedirs(os.path.dirname(dest_path), exist_ok=True)
  with codecs.open(source_path, "r", "utf-8") as in_file, codecs.open(dest_path, "w", "utf-8") as out_file:
    text = in_file.read()
    while text:
      if source_script == "TAMIL":
        out_text = transliterate_tamil(text, dest_script, pre_options, post_options)
      else:
        out_text = aksharamukha.transliterate.process(src=source_script, tgt=dest_script, txt=text, nativize = True, pre_options = pre_options, post_options = post_options)
      out_file.write(out_text)
      if source_path != dest_path:
        text = in_file.read()


def manipravaalify(text):
  from indic_transliteration.sanscript import schemes
  typos_df = pandas.read_csv(os.path.join(os.path.dirname(schemes.__file__), "data/ta_sa/manual.tsv"), sep="\t")
  typos_df = typos_df.set_index("sa")
  for sa_word in tqdm.tqdm(typos_df.index):
    if isinstance(typos_df.loc[sa_word, "ta_csv"], pandas.Series):
      logging.fatal(f"typo-table has a duplicate - {sa_word}")
    ta_words = typos_df.loc[sa_word, "ta_csv"].split(",")
    for ta_word in ta_words:
      text = regex.sub(ta_word.strip(), sa_word.strip(), text)
  return text
