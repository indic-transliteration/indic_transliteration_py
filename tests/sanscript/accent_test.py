from indic_transliteration.sanscript.schemes.brahmic import accent
from indic_transliteration import sanscript


def test_move_accent_to_previous_syllable():
  devanagari = sanscript.SCHEMES[sanscript.DEVANAGARI]
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="सैॗषा᳘ निदा᳘नेना यदि᳘डा॥", old_accent="ॗ", new_accent="ॗ") == "ॗसैषा᳘ निदा᳘नेना यदि᳘डा॥"
  assert accent.add_accent_to_previous_syllable(scheme=devanagari, text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।", old_accent="᳕", new_accent="ॗ") == "तॖस्माद्वाॖ अप॑ उॖपस्पृशतिॗ॥ सोऽग्निॖमेॗवाभीॖक्षमाणः।".replace("ॖ", "॑")


def test_set_diirgha_svaritas():
  assert accent.set_diirgha_svaritas(scheme=sanscript.SCHEMES[sanscript.DEVANAGARI], text="त॑स्माद्वा॑ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी॑क्षमाणः।") == "त॑स्माद्वा᳚ अप॑ उ॑पस्पृशति॥ सो᳕ऽग्नि॑मेवा᳕भी᳚क्षमाणः।"
  
  
def test_to_US_accents():
  assert accent.to_US_accents(text="""ध्रु॒वो॑ऽसि ।  \nध्रु॒वो॒॑ऽहँ स॑जा॒तेषु॑+++(=haya)+++ भूयास॒न्  \nधीर॒श् चेत्ता॑ वसु॒वित्।""") == "ध्रुवो᳕ऽसि ।  \nध्रुवो꣡ऽहँ꣡ सजाते꣡षु+++(=haya)+++ भूयासन्  \nधी꣡रश् चे꣡त्ता वसुवि꣡त्।"
  assert accent.to_US_accents(text="\"यज॑मानेन॒ खलु॒ वै तत् का॒र्य॑म्\" इत्य् आ॑हु॒र्") == "\"य꣡जमानेन ख꣡लु वै꣡ त꣡त् कार्य᳕म्\" इ꣡त्य् आहुर्"
  
  assert accent.to_US_accents(text="\"स त्वा+++(←तु + वै)+++ इडा॒म् उप॑ह्वयेत॒,") == "\"स꣡ त्वा꣡+++(←तु + वै)+++ इ꣡डाम् उ꣡पह्वयेत,"
  assert accent.to_US_accents(text="ए॒तत्प्रति॒ वा असु॑राणाय्ँ य॒ज्ञो व्य॑च्छिद्यत ।  ") == "एत꣡त्प्र꣡ति वा꣡ अ꣡सुराणाय्ँ यज्ञो꣡ व्यच्छिद्यत ।  "
