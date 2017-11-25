Indic transliteration tools
=======================
[![Build Status](https://travis-ci.org/sanskrit-coders/indic_transliteration.svg?branch=master)](https://travis-ci.org/sanskrit-coders/indic_transliteration)
[![Documentation Status](https://readthedocs.org/projects/indic-transliteration/badge/?version=latest)](http://indic-transliteration.readthedocs.io/en/latest/?badge=latest)


# For users
For detailed examples and help, please see individual module files in this package.

## Installation or upgrade:
* `sudo pip install indic_transliteration -U`
* `sudo pip install git+https://github.com/sanskrit-coders/indic_transliteration/@master -U`
* [Web](https://pypi.python.org/pypi/indic-transliteration).
* [Docs](http://indic-transliteration.readthedocs.io/en/latest/).

# For contributors
## Contact
Have a problem or question? Please head to [github](https://github.com/sanskrit-coders/indic_transliteration).

## Packaging
* ~/.pypirc should have your pypi login credentials.
```
python setup.py bdist_wheel
twine upload dist/* --skip-existing
```