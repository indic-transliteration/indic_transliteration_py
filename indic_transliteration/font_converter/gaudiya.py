import re
import unicodedata


CHAR_MAP = str.maketrans({
  # vowels
  "Ä": "Ā", "ä": "ā",
  "É": "Ī", "é": "ī",
  "Ü": "Ū", "ü": "ū",
  "Å": "Ṛ", "å": "ṛ",

  # consonants
  "Ç": "Ś", "ç": "ś",
  "Ö": "Ṭ", "ö": "ṭ",
  "Ò": "Ḍ", "ò": "ḍ",
  "Ë": "Ṇ", "ë": "ṇ",
  "Ì": "Ṅ", "ì": "ṅ",
  "Ï": "Ñ", "ï": "ñ",

  # anusvāra / visarga
  "À": "Ṃ", "à": "ṃ",
  "Ù": "Ḥ", "ù": "ḥ",
})


WORD_FIXES = {
  # extremely common words in Gaudiya texts
  "Çré": "Śrī",
  "Çréla": "Śrīla",
  "Çrémad": "Śrīmad",
  "Çrémän": "Śrīmān",

  "Kåñëa": "Kṛṣṇa",
  "kåñëa": "kṛṣṇa",

  "Vaiñëava": "Vaiṣṇava",
  "vaiñëava": "vaiṣṇava",

  "Viñëu": "Viṣṇu",
  "viñëu": "viṣṇu",

  "Öhäkura": "Ṭhākura",
  "öhäkura": "ṭhākura",

  "Våndävana": "Vṛndāvana",
  "Navadvépa": "Navadvīpa",

  "Mahäprabhu": "Mahāprabhu",
  "Jähnavä": "Jāhnavā",
  "Gétä": "Gītā",

  "gauraìga": "gaurāṅga",
  "Gauraìga": "Gaurāṅga",

  "saìkértana": "saṅkīrtana",
  "Saìkértana": "Saṅkīrtana",

  "paëòita": "paṇḍita",
  "Paëòita": "Paṇḍita",

  "maëòala": "maṇḍala",
  "Maëòala": "Maṇḍala",

  "daëòa": "daṇḍa",
  "Daëòa": "Daṇḍa",
}


def to_iast(text: str) -> str:
  # OCR cruft
  text = text.replace("́", "")
  text = text.replace("\\-", "-")
  text = text.replace("\\[", "[")
  text = text.replace("\\]", "]")

  # character-level conversion
  text = text.translate(CHAR_MAP)

  # word-level fixes
  for old, new in WORD_FIXES.items():
    text = text.replace(old, new)

  # Sanskrit clusters often mangled after the basic conversion
  regex_fixes = [
    (r"kṛṣñ", "kṛṣṇ"),
    (r"viṣñ", "viṣṇ"),
    (r"vaiṣñ", "vaiṣṇ"),
    ("bhūñaṇa", "bhūṣaṇa"),
    (r"jñ", "jñ"),
    (r"kṣ", "kṣ"),
    (r"ñ(?=[ṭyṇmv])", "ṣ")
  ]

  for pat, repl in regex_fixes:
    text = re.sub(pat, repl, text)

  # normalize Unicode + whitespace
  text = unicodedata.normalize("NFC", text)
  text = re.sub(r"[ \t]+", " ", text)
  text = re.sub(r"\n{3,}", "\n\n", text)

  return text