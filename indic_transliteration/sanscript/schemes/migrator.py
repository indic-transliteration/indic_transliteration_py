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
  for old_path in old_files:
    logging.info(old_path)
    with codecs.open(old_path, "r", 'utf-8') as file_in:
      scheme = json.load(file_in)
    new_path = old_path.replace(source_dir, dest_dir).replace(".json", ".toml")
    os.makedirs(name=os.path.dirname(new_path), exist_ok=True)
    with codecs.open(new_path, "w", 'utf-8') as file_in:
      toml.dump(scheme, file_in)


if __name__ == '__main__':
  migrate(source_dir=os.path.join(os.path.dirname(__file__), "data"), dest_dir=os.path.join(os.path.dirname(__file__), "data_toml"))