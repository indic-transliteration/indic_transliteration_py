import codecs
import glob
import json
import logging
import os
# Remove all handlers associated with the root logger object.
import toml

for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

SCHEMES = {}

def migrate(source_dir, dest_dir):
  old_files = glob.glob(os.path.join(source_dir, "**/*.json"))
  with codecs.open(os.path.join(source_dir, "brahmic/devanagari.json"), "r", 'utf-8') as file_in:
    devanagari_scheme = json.load(file_in)
    for old_path in old_files:
      new_path = old_path.replace(source_dir, dest_dir).replace(".json", ".toml")
      logging.info("%s → %s", os.path.basename(old_path), os.path.basename(new_path))
      os.makedirs(name=os.path.dirname(new_path), exist_ok=True)
      with codecs.open(old_path, "r", 'utf-8') as file_in, codecs.open(new_path, "w", 'utf-8') as file_out:
        scheme = json.load(file_in)
        new_scheme = {}
        for key in scheme:
          if key in devanagari_scheme and not key.startswith("alternate"):
            new_scheme[key] = dict(zip(devanagari_scheme[key], scheme[key]))
          else:
            new_scheme[key] = scheme[key]
        toml.dump(new_scheme, file_out)


if __name__ == '__main__':
  migrate(source_dir=os.path.join(os.path.dirname(__file__), "data"), dest_dir=os.path.join(os.path.dirname(__file__), "toml"))