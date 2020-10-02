

def test_language_code_to_script():
    from indic_transliteration import language_code_to_script
    assert language_code_to_script["sa"] == "devanagari"