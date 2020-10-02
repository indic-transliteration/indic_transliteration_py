"""
:py:mod:`~indic_transliteration.sanscript` is the most popular submodule here.
"""
import json
import os

language_code_to_script = json.load(os.path.join(os.dirname(__file__), "language_code_to_script.json"))