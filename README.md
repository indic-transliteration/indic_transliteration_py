Indic transliteration tools
=======================
[![Build Status](https://travis-ci.org/sanskrit-coders/indic_transliteration.svg?branch=master)](https://travis-ci.org/sanskrit-coders/indic_transliteration)
[![Documentation Status](https://readthedocs.org/projects/indic-transliteration/badge/?version=latest)](http://indic-transliteration.readthedocs.io/en/latest/?badge=latest)


# For users
* [Docs](http://indic-transliteration.readthedocs.io/en/latest/).
* For detailed examples and help, please see individual module files in this package.

## Installation or upgrade:
* `sudo pip install indic_transliteration -U`
* `sudo pip install git+https://github.com/sanskrit-coders/indic_transliteration/@master -U`
* [Web](https://pypi.python.org/pypi/indic-transliteration).


## Usage

```py
In [1]: from indic_transliteration import sanscript
   ...: from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
   ...:

In [2]: data = 'idam adbhutam'

In [3]: print(transliterate(data, sanscript.HK, sanscript.TELUGU))
ఇదమ్ అద్భుతమ్

In [4]: print(transliterate(data, sanscript.ITRANS, sanscript.DEVANAGARI))
इदम् अद्भुतम्

In [5]: scheme_map = SchemeMap(SCHEMES[sanscript.VELTHUIS], SCHEMES[sanscript.TELUGU])

In [6]: print(transliterate(data, scheme_map=scheme_map))
ఇదమ్ అద్భుతమ్
```

## Dravidian language extension
```py
In [1]: from indic_transliteration import xsanscript
   ...: from indic_transliteration.xsanscript import SchemeMap, SCHEMES, transliterate
   ...:

In [2]: data = 'असय औषधिः ग्रन्थः। ऎ ऒ यॆक्ककॊ?'

In [3]: print(transliterate(data, xsanscript.DEVANAGARI, xsanscript.KANNADA))
ಅಸಯ ಔಷಧಿಃ ಗ್ರನ್ಥಃ। ಎ ಒ ಯೆಕ್ಕಕೊ?
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
