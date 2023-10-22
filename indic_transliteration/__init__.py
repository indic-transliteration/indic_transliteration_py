"""
:py:mod:`~indic_transliteration.sanscript` is the most popular submodule here.
"""
import json
import os


language_code_to_script = {}

with open(os.path.join(os.path.dirname(__file__), "sanscript/schemes/data/language_code_to_script.json")) as f:
    language_code_to_script = json.load(f)



