from typing import Optional

import typer
from indic_transliteration.sanscript import transliterate, SCHEMES, SchemeMap

from indic_transliteration.sanscript_cli import typer_opts
from indic_transliteration.sanscript_cli.help_text import program as program_help
from indic_transliteration.sanscript_cli.utils import get_input_data, write_output

app = typer.Typer()


@app.command(no_args_is_help=True, help=program_help)
def main(
    from_scheme: str = typer_opts.from_scheme,
    to_scheme: str = typer_opts.to_scheme,
    input_file: Optional[typer.FileText] = typer_opts.input_file,
    output_file: Optional[typer.FileTextWrite] = typer_opts.output_file,
    input_string: Optional[str] = typer_opts.input_string,
):
    scheme_map = SchemeMap(SCHEMES[from_scheme], SCHEMES[to_scheme])
    input_data = get_input_data(input_file, input_string)

    output_data = transliterate(input_data, scheme_map=scheme_map)
    write_output(output_file, output_data)
