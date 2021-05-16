import sys
from os import path

import typer

SUCCESS_COLOR = typer.colors.GREEN
WARNING_COLOR = typer.colors.YELLOW
ERROR_COLOR = typer.colors.BRIGHT_RED


def show_info(msg: str):
    typer.echo(msg)


def show_success(msg: str):
    typer.secho(msg, fg=SUCCESS_COLOR, err=True)


def show_warning(msg: str):
    typer.secho(msg, fg=WARNING_COLOR, err=True)


def show_error(msg: str):
    typer.secho(msg, fg=ERROR_COLOR, err=True)


def get_input_data(input_file: typer.FileText, input_string: str) -> str:
    if input_file is not None:
        if input_string is not None:
            show_warning(
                "Warning: The input string is ignored since input file is specified."
            )
        return input_file.read()

    if input_string is not None:
        return input_string

    show_error("Error: Either a string or a file is required as input.")
    show_info("See help (--help) for more info.")
    raise typer.Exit(code=1)


def write_output(output_file: typer.FileTextWrite, output_data: str):
    if output_file is None:
        return typer.echo(output_data)

    output_file.write(output_data)

    if output_file is sys.stdout:
        return

    show_success(f"Output written to: {path.realpath(output_file.name)}")
