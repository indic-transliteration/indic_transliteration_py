# -*- coding: utf-8 -*-
"""
test.sanscript
~~~~~~~~~~~~~~

Tests Sanskrit transliteration.

:license: MIT and BSD
"""

from __future__ import unicode_literals

import logging

import pytest

from indic_transliteration import sanscript
# Remove all handlers associated with the root logger object.
from indic_transliteration.sanscript.schemes import roman

for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)
logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(filename)s:%(lineno)d %(message)s"
)

DATA = {
  sanscript.BENGALI: {
    'vowels': 'অ আ ই ঈ উ ঊ ঋ ৠ ঌ ৡ এ ঐ ও ঔ',
    'marks': 'ক খা গি ঘী ঙু চূ ছৃ জৄ ঝৢ ঞৣ টে ঠৈ ডো ঢৌ ণং তঃ থ্',
    'consonants': """ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম
                         য র ল ব শ ষ স হ ळ""",
    'symbols': 'ॐ । ॥ ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯',
    'putra': 'পুত্র',
    'naraIti': 'নর ইতি',
    'sentence': 'ধর্মক্ষেত্রে কুরুক্ষেত্রে সমবেতা যুযুত্সবঃ ।'
  },
  sanscript.DEVANAGARI: {
    'vowels': 'अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ',
    'marks': 'क खा गि घी ङु चू छृ जॄ झॢ ञॣ टे ठै डो ढौ णं तः थ्',
    'consonants': """क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म
                         य र ल व श ष स ह ळ""",
    'symbols': 'ॐ । ॥ ० १ २ ३ ४ ५ ६ ७ ८ ९',
    'putra': 'पुत्र',
    'naraIti': 'नर इति',
    'sentence': 'धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः ।'
  },
  sanscript.GUJARATI: {
    'vowels': 'અ આ ઇ ઈ ઉ ઊ ઋ ૠ ઌ ૡ એ ઐ ઓ ઔ',
    'marks': 'ક ખા ગિ ઘી ઙુ ચૂ છૃ જૄ ઝૢ ઞૣ ટે ઠૈ ડો ઢૌ ણં તઃ થ્',
    'consonants': """ક ખ ગ ઘ ઙ ચ છ જ ઝ ઞ ટ ઠ ડ ઢ ણ ત થ દ ધ ન પ ફ બ ભ મ
                         ય ર લ વ શ ષ સ હ ળ""",
    'symbols': 'ૐ । ॥ ૦ ૧ ૨ ૩ ૪ ૫ ૬ ૭ ૮ ૯',
    'putra': 'પુત્ર',
    'naraIti': 'નર ઇતિ',
    'sentence': 'ધર્મક્ષેત્રે કુરુક્ષેત્રે સમવેતા યુયુત્સવઃ ।'
  },
  sanscript.TITUS: {
    'vowels': 'a ā i ī u ū r̥ r̥̄ l̥ l̥̄ e ai o au',
    'marks': 'ka kʰā gi gʰī ṅu cū cʰr̥ jr̥̄ jʰl̥ ñl̥̄ ṭe ṭʰai ḍo ḍʰau ṇaṃ taḥ tʰ',
    'consonants': """ka kʰa ga gʰa ṅa ca cʰa ja jʰa ña ṭa ṭʰa ḍa ḍʰa ṇa ta tʰa da dʰa na pa pʰa ba bʰa ma
    ya ra la va śa ṣa sa ha ḷa""",
    'symbols': 'oṃ . .. 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dʰarmakṣetre kurukṣetre samavetā yuyutsavaḥ .'
  },
  sanscript.HK: {
    'vowels': 'a A i I u U R RR lR lRR e ai o au',
    'marks': """ka khA gi ghI Gu cU chR jRR jhlR JlRR Te Thai Do Dhau
                    NaM taH th""",
    'consonants': """ka kha ga gha Ga ca cha ja jha Ja Ta Tha Da Dha Na
                         ta tha da dha na pa pha ba bha ma
                         ya ra la va za Sa sa ha La""",
    'symbols': 'OM | || 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dharmakSetre kurukSetre samavetA yuyutsavaH |'
  },
  sanscript.ITRANS: {
    'vowels': 'a A i I u U RRi RRI LLi LLI e ai o au',
    'marks': """ka khA gi ghI ~Nu chU ChRRi jRRI jhLLi ~nLLI Te Thai Do Dhau
                    NaM taH th""",
    'consonants': """ka kha ga gha ~Na cha Cha ja jha ~na Ta Tha Da Dha Na
                         ta tha da dha na pa pha ba bha ma
                         ya ra la va sha Sha sa ha La""",
    'symbols': 'OM | || 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dharmakShetre kurukShetre samavetA yuyutsavaH |'
  },
  sanscript.OPTITRANS: {
    'vowels': 'a A i I u U R RR LLi LLI e ai o au',
    'marks': """ka khA gi ghI ~Nu chU ChR jRR jhLLi ~nLLI Te Thai Do Dhau
                    NaM taH th""",
    'consonants': """ka kha ga gha ~Na cha Cha ja jha ~na Ta Tha Da Dha Na
                         ta tha da dha na pa pha ba bha ma
                         ya ra la va sha Sha sa ha La""",
    'symbols': 'OM | || 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dharmaxetre kuruxetre samavetA yuyutsavaH |'
  },
  sanscript.VELTHUIS: {
    'vowels': 'a aa i ii u uu .r .rr .l .ll e ai o au',
    'marks': """ka khaa gi ghii "nu cuu ch.r j.rr jh.l ~n.ll .te .thai .do .dhau
                    .na.m ta.h th""",
    'consonants': """ka kha ga gha "na ca cha ja jha ~na .ta .tha .da .dha .na
                         ta tha da dha na pa pha ba bha ma
                         ya ra la va "sa .sa sa ha La""",
    'symbols': 'O | || 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dharmak.setre kuruk.setre samavetaa yuyutsava.h |'
  },
  sanscript.IAST: {
    'vowels': 'a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au',
    'marks': 'ka khā gi ghī ṅu cū chṛ jṝ jhḷ ñḹ ṭe ṭhai ḍo ḍhau ṇaṃ taḥ th',
    'consonants': """ka kha ga gha ṅa ca cha ja jha ña ṭa ṭha ḍa ḍha ṇa
                         ta tha da dha na pa pha ba bha ma
                         ya ra la va śa ṣa sa ha ḻa""",
    'symbols': 'oṃ | || 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dharmakṣetre kurukṣetre samavetā yuyutsavaḥ |'
  },
  sanscript.KOLKATA: {
    'vowels': 'a ā i ī u ū ṛ ṝ ḷ ḹ ē ai ō au',
    'marks': 'ka khā gi ghī ṅu cū chṛ jṝ jhḷ ñḹ ṭē ṭhai ḍō ḍhau ṇaṃ taḥ th',
    'consonants': """ka kha ga gha ṅa ca cha ja jha ña ṭa ṭha ḍa ḍha ṇa
                         ta tha da dha na pa pha ba bha ma
                         ya ra la va śa ṣa sa ha ḻa""",
    'symbols': 'oṃ | || 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'dharmakṣētrē kurukṣētrē samavētā yuyutsavaḥ |'
  },
  sanscript.KANNADA: {
    'vowels': 'ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೠ ಌ ೡ ಏ ಐ ಓ ಔ',
    'marks': 'ಕ ಖಾ ಗಿ ಘೀ ಙು ಚೂ ಛೃ ಜೄ ಝೢ ಞೣ ಟೇ ಠೈ ಡೋ ಢೌ ಣಂ ತಃ ಥ್',
    'consonants': """ಕ ಖ ಗ ಘ ಙ ಚ ಛ ಜ ಝ ಞ ಟ ಠ ಡ ಢ ಣ ತ ಥ ದ ಧ ನ ಪ ಫ ಬ ಭ ಮ
                         ಯ ರ ಲ ವ ಶ ಷ ಸ ಹ ಳ""",
    'symbols': 'ಓಂ । ॥ ೦ ೧ ೨ ೩ ೪ ೫ ೬ ೭ ೮ ೯',
    'putra': 'ಪುತ್ರ',
    'naraIti': 'ನರ ಇತಿ',
    'sentence': 'ಧರ್ಮಕ್ಷೇತ್ರೇ ಕುರುಕ್ಷೇತ್ರೇ ಸಮವೇತಾ ಯುಯುತ್ಸವಃ ।'
  },
  sanscript.MALAYALAM: {
    'vowels': 'അ ആ ഇ ഈ ഉ ഊ ഋ ൠ ഌ ൡ ഏ ഐ ഓ ഔ',
    'marks': 'ക ഖാ ഗി ഘീ ങു ചൂ ഛൃ ജൄ ഝൢ ഞൣ ടേ ഠൈ ഡോ ഢൌ ണം തഃ ഥ്',
    'consonants': """ക ഖ ഗ ഘ ങ ച ഛ ജ ഝ ഞ ട ഠ ഡ ഢ ണ ത ഥ ദ ധ ന പ ഫ ബ ഭ മ
                         യ ര ല വ ശ ഷ സ ഹ ള""",
    'symbols': 'ഓം । ॥ ൦ ൧ ൨ ൩ ൪ ൫ ൬ ൭ ൮ ൯',
    'putra': 'പുത്ര',
    'naraIti': 'നര ഇതി',
    'sentence': 'ധര്മക്ഷേത്രേ കുരുക്ഷേത്രേ സമവേതാ യുയുത്സവഃ ।'
  },
  sanscript.SLP1: {
    'vowels': 'a A i I u U f F x X e E o O',
    'marks': 'ka KA gi GI Nu cU Cf jF Jx YX we WE qo QO RaM taH T',
    'consonants': """ka Ka ga Ga Na ca Ca ja Ja Ya wa Wa qa Qa Ra
                         ta Ta da Da na pa Pa ba Ba ma
                         ya ra la va Sa za sa ha La""",
    'symbols': 'oM . .. 0 1 2 3 4 5 6 7 8 9',
    'putra': 'putra',
    'naraIti': 'nara iti',
    'sentence': 'Darmakzetre kurukzetre samavetA yuyutsavaH .'
  },
  sanscript.WX: {
    'vowels': 'a A i I u U q Q L ḹ e E o O',
    'marks': 'ka KA gi GI fu cU Cq jQ JL Fḹ te TE do DO NaM waH W',
    'consonants': """ka Ka ga Ga fa ca Ca ja Ja Fa ta Ta da Da Na
                         wa Wa xa Xa na pa Pa ba Ba ma
                         ya ra la va Sa Ra sa ha ḻa""",
    'symbols': 'oM . .. 0 1 2 3 4 5 6 7 8 9',
    'putra': 'puwra',
    'naraIti': 'nara iwi',
    'sentence': 'XarmakRewre kurukRewre samavewA yuyuwsavaH .'
  },
  sanscript.TELUGU: {
    'vowels': 'అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ',
    'marks': 'క ఖా గి ఘీ ఙు చూ ఛృ జౄ ఝౢ ఞౣ టే ఠై డో ఢౌ ణం తః థ్',
    'consonants': """క ఖ గ ఘ ఙ చ ఛ జ ఝ ఞ ట ఠ డ ఢ ణ త థ ద ధ న ప ఫ బ భ మ
                         య ర ల వ శ ష స హ ళ""",
    'symbols': 'ఓం । ॥ ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯',
    'putra': 'పుత్ర',
    'naraIti': 'నర ఇతి',
    'sentence': 'ధర్మక్షేత్రే కురుక్షేత్రే సమవేతా యుయుత్సవః ।'
  }
}


def _compare_all_data_between_schemes(_from, _to):
  """Compare all data for `_from` and `_to`"""

  def compare_group(_from, _to, group):
    """Compare data for `_from` and `_to` in the test group `group`."""
    source = DATA[_from][group]
    actual = ' '.join(sanscript.transliterate(source, _from, _to).split())
    expected = ' '.join(DATA[_to][group].split())
    assert expected == actual, "Failure ahoy: %s to %s: expected %s, got %s" % (_from, _to, expected, actual)

  for group in DATA[_from]:
    if _to in DATA and group in DATA[_to]:
      compare_group(_from, _to, group)



@pytest.mark.parametrize("name", sanscript.SCHEMES)
def test_membership(name):
  """Test that a scheme is roman iff `is_roman`"""
  assert sanscript.SCHEMES[name].is_roman == (name in roman.ALL_SCHEME_IDS)


@pytest.mark.parametrize("name,scheme", sanscript.SCHEMES.items())
def test_correspondence(name, scheme ):
  """Test that schemes correspond to a subset of Devanagari.

  Since Devanagari is the most comprehensive scheme available, every
  scheme corresponds to a subset of Devanagari."""
  dev = sanscript.SCHEMES[sanscript.DEVANAGARI]
  groups = set(dev.keys())
  for group in scheme:
    logging.debug(name)
    logging.debug(group)
    assert group in groups


@pytest.mark.parametrize("from_scheme", roman.ALL_SCHEME_IDS)
@pytest.mark.parametrize("to_scheme", roman.ALL_SCHEME_IDS)
def test_to_roman(from_scheme, to_scheme):
  """Test roman to roman."""
  _compare_all_data_between_schemes(from_scheme, to_scheme)


@pytest.mark.parametrize("from_scheme", roman.ALL_SCHEME_IDS)
@pytest.mark.parametrize("to_scheme", sanscript.BRAHMIC_SCHEMES.keys())
def test_to_brahmic(from_scheme, to_scheme):
  """Test roman to Brahmic."""
  _compare_all_data_between_schemes(from_scheme, to_scheme)


def test_devanaagarii_equivalence():
  """Test all synonmous transliterations."""
  logging.info(sanscript.transliterate("rAmo gUDhaM vaktI~Ngitaj~naH kShetre", sanscript.ITRANS, sanscript.DEVANAGARI))
  assert sanscript.transliterate("rAmo gUDhaM vaktI~Ngitaj~naH kShetre", sanscript.ITRANS, sanscript.DEVANAGARI) == \
                   sanscript.transliterate("raamo guuDhaM vaktii~NgitaGYaH xetre", sanscript.ITRANS, sanscript.DEVANAGARI)


@pytest.mark.parametrize("to_scheme", roman.ALL_SCHEME_IDS)
def test_brahmic_to_roman(to_scheme):
  """Test Brahmic to roman."""
  from_scheme = sanscript.DEVANAGARI
  _compare_all_data_between_schemes(from_scheme, to_scheme)


@pytest.mark.parametrize("to_scheme", sanscript.BRAHMIC_SCHEMES.keys())
def test_devanagari_to_brahmic(to_scheme):
  """Test Brahmic to Brahmic."""
  from_scheme = sanscript.DEVANAGARI
  _compare_all_data_between_schemes(from_scheme, to_scheme)

@pytest.mark.parametrize("scheme_id", sanscript.BRAHMIC_SCHEMES.keys())
def test_vowel_to_mark_map(scheme_id):
  brahmic_scheme = sanscript.SCHEMES[scheme_id]
  assert brahmic_scheme.vowel_to_mark_map[brahmic_scheme.from_devanagari("अ")] == ""
  assert brahmic_scheme.vowel_to_mark_map[brahmic_scheme.from_devanagari("आ")] == brahmic_scheme.from_devanagari("ा")
  for vowel in "इ ई उ ऊ ए ऐ ओ औ".split(" "):
    assert brahmic_scheme.vowel_to_mark_map[brahmic_scheme.from_devanagari(vowel)] == brahmic_scheme.from_devanagari(sanscript.SCHEMES[sanscript.DEVANAGARI].vowel_to_mark_map[vowel]), vowel

## Toggle tests
def _toggle_test_helper(_from, _to):
  def func(data, output):
    assert output == sanscript.transliterate(data, _from, _to), "_from: %s, _to: %s, _input: %s" % (_from, _to, data)

  return func

def test_toggle():
  f = _toggle_test_helper(sanscript.HK, sanscript.DEVANAGARI)
  f('akSa##kSa##ra', 'अक्षkSaर')
  f('##akSa##kSa##ra', 'akSaक्षra')
  f('akSa##ra##', 'अक्षra')
  f('akSa##ra', 'अक्षra')
  f('akSa##kSa##ra####', 'अक्षkSaर')
  f('a####kSara', 'अक्षर')
  f('a#kSara', 'अ#क्षर')

def test_suspend():
  f = _toggle_test_helper(sanscript.HK, sanscript.DEVANAGARI)
  f('<p>nara iti</p>', '<p>नर इति</p>')

def test_suspend_and_toggle():
  f = _toggle_test_helper(sanscript.HK, sanscript.DEVANAGARI)
  f('<p>##na##ra## iti</p>', '<p>naर iti</p>')

