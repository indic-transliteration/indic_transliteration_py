"""
:py:mod:`~indic_transliteration.sanscript` is the most popular submodule here.
"""
import codecs
import json
import logging
import os


language_code_to_script = {}

with open(os.path.join(os.path.dirname(__file__), "language_code_to_script.json")) as f:
    language_code_to_script = json.load(f)



def convert_with_aksharamukha(source_path, dest_path, source_script, dest_script, pre_options = [], post_options = []):
  import aksharamukha.transliterate
  logging.info("\nTransliterating (%s > %s) %s to %s", source_script, dest_script, source_path, dest_path)
  os.makedirs(os.path.dirname(dest_path), exist_ok=True)
  with codecs.open(source_path, "r", "utf-8") as in_file, codecs.open(dest_path, "w", "utf-8") as out_file:
    text = in_file.read()
    while text:
      out_text = aksharamukha.transliterate.process(src=source_script, tgt=dest_script, txt=text, nativize = True, pre_options = pre_options, post_options = post_options)
      out_file.write(out_text)
      if source_path != dest_path:
        text = in_file.read()
