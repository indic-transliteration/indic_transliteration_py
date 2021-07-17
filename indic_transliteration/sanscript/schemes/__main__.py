import os.path

from indic_transliteration.sanscript.schemes import load_scheme

scheme = load_scheme(file_path=os.path.join(os.path.dirname(__file__), "data", "brahmic/devanagari.json"))
pass