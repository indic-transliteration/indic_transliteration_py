"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = ''
try:
  import pypandoc

  long_description = pypandoc.convert_file(source_file='README.md', to='rst', format='markdown_github')
except (IOError, ImportError):
  long_description = ''

with open('requirements.txt', 'r') as f:
  install_reqs = [
    s for s in [
      line.split('#', 1)[0].strip(' \t\n') for line in f
    ] if s != ''
  ]


with open('extras.txt', 'r') as f:
  install_extras = [
    s for s in [
      line.split('#', 1)[0].strip(' \t\n') for line in f
    ] if s != ''
  ]


setup(
  name='indic_transliteration',

  # Versions should comply with PEP440.  For a discussion on single-sourcing
  # the version across setup.py and the project code, see
  # https://packaging.python.org/en/latest/single_source_version.html
  version='2.3.69',


  description='Transliteration tools to convert text in one indic script encoding to another',
  long_description=long_description,

  # The project's main homepage.
  url='https://github.com/indic-transliteration/indic_transliteration_py',

  # Author details
  author='Sanskrit programmers',
  author_email='sanskrit-programmers@googlegroups.com',

  # Choose your license
  license='MIT',

  # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Natural Language :: Hindi',
    'Natural Language :: Tamil',
    'Natural Language :: Bengali',
    'Natural Language :: Panjabi',
    'Natural Language :: Marathi',
    'Topic :: Text Processing :: Linguistic',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3'
  ],

  # What does your project relate to?
  keywords='indic script transliteration hindi sanskrit samskritam kannada devanagari tamil malayalam telugu gurumukhi gujarati bengali oriya - Harvard-Kyoto IAST Roman-Unicode) SLP1 WX',

  # You can just specify the packages manually here if your project is
  # simple. Or you can use find_packages().
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),

  # Alternatively, if you want to distribute just a my_module.py, uncomment
  # this:
  #   py_modules=["my_module"],

  # List run-time dependencies here.  These will be installed by pip when
  # your project is installed. For an analysis of "install_requires" vs pip's
  # requirements files see:
  # https://packaging.python.org/en/latest/requirements.html
  install_requires=install_reqs,

  # List additional groups of dependencies here (e.g. development
  # dependencies). You can install these using the following syntax,
  # for example:
  # $ pip install -e .[dev,test]
  extras_require={
    # 'dev': ['check-manifest'],
    'test': ['pytest'],
    'extras': install_extras,
  },

  include_package_data = True,

  # If there are data files included in your packages that need to be
  # installed, specify them here.  If using Python 2.6 or less, then these
  # have to be included in MANIFEST.in as well.
  # package_data={
  #     'sample': ['package_data.dat'],
  # },

  # Although 'package_data' is the preferred approach, in some case you may
  # need to place data files outside of your packages. See:
  # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
  # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
  # data_files=[('my_data', ['data/data_file'])],

  # To provide executable scripts, use entry points in preference to the
  # "scripts" keyword. Entry points provide cross-platform support and allow
  # pip to create the appropriate form of executable for the target platform.
  entry_points={
      'console_scripts': [
          'sanscript=indic_transliteration.sanscript_cli:app',
      ],
  },
)
