import typer
from indic_transliteration.sanscript import SCHEMES

from indic_transliteration.sanscript_cli import help_text

scheme_names = list(SCHEMES.keys())
scheme_help = "Choose from: {}.".format(", ".join(scheme_names))


def complete_scheme_name(incomplete: str):
    for scheme_name in scheme_names:
        if scheme_name.startswith(incomplete):
            yield scheme_name


def check_scheme(scheme_name: str):
    if scheme_name in scheme_names:
        return scheme_name

    error_msg = f"Invalid scheme name. \n\n{scheme_help}"
    raise typer.BadParameter(error_msg)


from_scheme = typer.Option(
    ...,
    "--from",
    "-f",
    help=help_text.from_scheme,
    callback=check_scheme,
    autocompletion=complete_scheme_name,
)

to_scheme = typer.Option(
    ...,
    "--to",
    "-t",
    help=help_text.to_scheme,
    callback=check_scheme,
    autocompletion=complete_scheme_name,
)

input_file = typer.Option(
    None,
    "--input-file",
    "-i",
    help=help_text.input_file,
)

output_file = typer.Option(None, "--output-file", "-o", help=help_text.output_file)

input_string = typer.Argument(
    None,
    help=help_text.input_string,
)
