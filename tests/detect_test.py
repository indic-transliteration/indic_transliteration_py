# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Tests for detect.py

    :license: MIT and BSD
"""

import pytest
import sys

from indic_transliteration.detect import detect, Scheme as S


def add(testcases, scheme, items):
    testcases.extend([(x, scheme) for x in items])


BASIC = []
add(BASIC, S.Bengali, ['অ', '৺'])
add(BASIC, S.Devanagari, ['ऄ', 'ॿ'])
add(BASIC, S.Gujarati, ['અ', '૱'])
add(BASIC, S.Gurmukhi, ['ਅ', 'ੴ'])
add(BASIC, S.Kannada, ['ಅ', '೯'])
add(BASIC, S.Malayalam, ['അ', 'ൿ'])
add(BASIC, S.Oriya, ['ଅ', 'ୱ'])
add(BASIC, S.Tamil, ['அ', '௺'])
add(BASIC, S.Telugu, ['అ', '౿'])
add(BASIC, S.HK, [
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
add(BASIC, S.IAST, [
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
add(BASIC, S.ITRANS, [
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
add(BASIC, S.Kolkata, [
    'tējas',
    'sōma',
])
add(BASIC, S.SLP1, [
    'kfta',
    'pitFn',
    'kxpta',
    'XkAra',
    'kEvalya',
    'kOsalya',
    'Gasmara',
    'GAsa',
    'Guka',
    'GUr',
    'Gfta',
    'Goza',
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
add(BASIC, S.Velthuis, [
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
    if sys.version_info >= (3,0):
        text = text.decode('utf-8')
    detection = detect(text)
    assert detection == scheme, u'%s == %s (%s)' % (detection, scheme, text)


@pytest.mark.parametrize('data', BASIC)
def test_noisy(data):
    noise = ' \t\n 1234567890 !@#$%^&*(),.<>\'\"-_[]{}\\|;:`~ ΣД あア'
    text, scheme = data
    text = ''.join([noise, text, noise])
    assert detect(text) == scheme
