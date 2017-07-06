Indic transliteration tools
=======================
# Intro
For detailed examples and help, please see individual module files in this package.

Installation or upgrade:
* `sudo pip2 install indic_transliteration -U`
* [Web](https://pypi.python.org/pypi/indic-transliteration).

# Transliteration
```
from indic_transliteration import sanscript
output = sanscript.transliterate('idam adbhutam', sanscript.HK, sanscript.DEVANAGARI)
sanscript.transliterate(u"गच्छ",sanscript.DEVANAGARI, sanscript.HK)
```

# Script detection
`detect.py` automatically detects a string's transliteration scheme:
```
from indic_transliteration import detect
detect.detect('pitRRIn') == Scheme.ITRANS
detect.detect('pitRRn') == Scheme.HK
```

# For contributors
## Contact
Have a problem or question? Please head to [github](https://github.com/sanskrit-coders/indic_transliteration).

## Packaging
* ~/.pypirc should have your pypi login credentials.
```
python setup.py bdist_wheel
twine upload dist/* --skip-existing
```