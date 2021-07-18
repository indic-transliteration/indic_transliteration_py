from indic_transliteration.sanscript import roman
from indic_transliteration.sanscript.schemes import brahmic

ROMAN_SCHEMES = roman.SCHEMES

program = f"""
A CLI for indic script transliteration based on "indic-transliteration" python library.

Supported scripts/schemes:

- Brahmic scripts: {", ".join(list(brahmic.SCHEMES.keys()))}

- Romanizations: {", ".join(list(ROMAN_SCHEMES.keys()))}

Input can be:

- from command's argument

    Example:  $ sanscript --from hk --to iast "rAmAyaNa"      
    
    Output:   rāmāyaṇa

- from file passed to '--input-file / -i' option

    Example:  $ sanscript --from hk --to iast -i ramayana.txt
    
    Output:   rāmāyaṇa

- from Standard Input using '-'

    Example:  $ cat ramayana.txt | sanscript --from hk --to iast -i -
    
    OR:       $ sanscript --from hk --to iast -i - < ramayana.txt
    
    Output:   rāmāyaṇa

Output can be:

- to Standard Output

    Example:  $ sanscript --from hk --to iast "rAmAyaNa"      
    
    OR:       $ sanscript --from hk --to iast "rAmAyaNa" -o -
    
    Output:   rāmāyaṇa

- to file passed to '--ouput-file / -o' option

    Example:  $ sanscript --from hk --to iast "rAmAyaNa" -o output.txt
    
    Output:   Output written to: /home/user/output.txt

For more info: https://github.com/indic-transliteration/indic_transliteration_py
"""

from_scheme = """
Name of the scheme FROM which the input is to be transliterated.
See supported schemes list given above.
"""

to_scheme = """
Name of the scheme TO which the input is to be transliterated.
See supported schemes list given above.
"""

output_file = """
Output file path to write transliterated output. Note: If it is not specified
or its argument is '-', the output is written to Standard Output.
"""

input_file = """
Input file path to transliterate. Note: When this option is used, input from
the INPUT_STRING argument will be ignored.
"""

input_string = """
Input string to transliterate from the given '--from' scheme to the given
'--to' scheme. Note: This input will be ignored if '--input-file' option is
specified.
"""
