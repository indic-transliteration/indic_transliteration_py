# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Tests for detect.py

    :license: MIT and BSD
"""

import pytest
import sys

from indic_transliteration.detect import detect, Scheme


def add(testcases, scheme, items):
    testcases.extend([(x, scheme) for x in items])


BASIC = []
add(BASIC, Scheme.Bengali, ['অ', '৺'])
add(BASIC, Scheme.Devanagari, ['ऄ', 'ॿ'])
add(BASIC, Scheme.Gujarati, ['અ', '૱'])
add(BASIC, Scheme.Gurmukhi, ['ਅ', 'ੴ'])
add(BASIC, Scheme.Kannada, ['ಅ', '೯'])
add(BASIC, Scheme.Malayalam, ['അ', 'ൿ'])
add(BASIC, Scheme.Oriya, ['ଅ', 'ୱ'])
add(BASIC, Scheme.Tamil, ['அ', '௺'])
add(BASIC, Scheme.Telugu, ['అ', '౿'])
add(BASIC, Scheme.HK, [
    '',
    'rAga',
    'nadI',
    'vadhU',
    'kRta',
    'pitRRn',
    'klRpta',
    'lRR',
    'tejasvI',
    'gomayaH',
    'haMsa',
    'naraH',
    'aGka',
    'aGga',
    'prAGnayana',
    'vAGmaya',
    'aJjana',
    'kuTumba',
    'kaThora',
    'Damaru',
    'soDhA',
    'aruNa',
    'zveta',
    'SaS',
    'pANDava',
    'zRNoti',
    'jJAna',
    'gacchati',
    'SaNmAsa',
    'pariNata',
    'aruNa',
    'reNu',
    'koNa',
    'karaNa',
    'akSa',
    'antazcarati',
    'prazna',
    'azvatthAman',
    'yuddha',
])
add(BASIC, Scheme.IAST, [
    'rāga',
    'nadī',
    'vadhū',
    'kṛta',
    'pitṝn',
    'kḷpta',
    'ḹ',
    'tejasvī',
    'gomayaḥ',
    'haṃsa',
    'naraḥ',
    'aṅga',
    'añjana',
    'kuṭumba',
    'kaṭhora',
    'ḍamaru',
    'soḍhā',
    'aruṇa',
    'śveta',
    'ṣaṣ',
    'ḻa',
    'pāṇḍava',
    'śṛṇoti',
    'jñāna',
])
add(BASIC, Scheme.ITRANS, [
    'raaga',
    'nadii',
    'nadee',
    'vadhuu',
    'vadhoo',
    'kRRita',
    'kR^ita',
    'pitRRIn',
    'pitR^In',
    'kLLipta',
    'kL^ipta',
    'LLI',
    'L^I',
    'a~Nga',
    'aN^ga',
    'ChAyA',
    'chhAyA',
    'a~njana',
    'aJNjana',
    'shveta',
    'ShaSh',
    'shhashh',
    '.akarot',
    'shRRiNoti',
    'j~nAna',
    'gachChati',
    'gachchhati',
])
add(BASIC, Scheme.Kolkata, [
    'tējas',
    'sōma',
])
add(BASIC, Scheme.SLP1, [
    'kfta',
    'pitFn',
    'kxpta',
    'XkAra',
    'kEvalya',
    'kOsalya',
    # The below could be HK.
    # 'Gasmara',
    # 'GAsa',
    # 'Guka',
    # 'GUr',
    'Gfta',
    # The below could be HK.
    # 'Goza',
    'GOra',
    'arGya',
    'GrA',
    'aNka',
    'aNga',
    'CAyA',
    'aYjana',
    'jYAna',
    'kuwumba',
    'kaWora'
    'qamaru',
    'soQA',
    'pARqava',
    'Pala',
    'Bara',
    'gacCati',
    'zaRmAsa',
    'pariRata',
    'aruRa',
    'SfRoti',
    'reRu',
    'koRa',
    'ArDadrORika',
    'akza',
    'antaScarati',
    'praSna',
    'aSvatTAman',
    'yudDa',
])
add(BASIC, Scheme.Velthuis, [
    'k.rta',
    'pit.rrn',
    'k.lipta',
    '.ll',
    'sa.myoga',
    'gomaya.h',
    'a"nga',
    'ku.tumba',
    'ka.thora',
    '.damaru',
    'so.dhaa',
    'aru.na',
    '~sveta',
    '.sa.s',
])


@pytest.mark.parametrize('data', BASIC)
def test_basic(data):
    text, scheme = data
    detection = detect(text)
    assert detection == scheme, u'%s == %s (%s)' % (detection, scheme, text)


@pytest.mark.parametrize('data', BASIC)
def test_decoded(data):
    text, scheme = data
    if sys.version_info < (3,0):
        text = text.decode('utf-8')
    detection = detect(text)
    assert detection == scheme, u'%s == %s (%s)' % (detection, scheme, text)

# Below is failing for Py 3 - HK/ SLP1 confusion - https://travis-ci.org/sanskrit-coders/indic_transliteration/jobs/306990133
# @pytest.mark.skipif(sys.version_info > (3,0), reason="Below is failing for Py 3 - HK/ SLP1 confusion.")
@pytest.mark.parametrize('data', BASIC)
def test_noisy(data):
    noise = ' \t\n 1234567890 !@#$%^&*(),.<>\'\"-_[]{}\\|;:`~ ΣД あア'
    text, scheme = data
    text = ''.join([noise, text, noise])
    assert detect(text) == scheme, data
