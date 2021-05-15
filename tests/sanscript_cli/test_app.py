from typer.testing import CliRunner

from indic_transliteration.sanscript_cli import app

runner = CliRunner()

test_input = "rAmAyaNa"
expected_output = "rāmāyaṇa"


def test_argument_input():
    result = runner.invoke(app, ["--from", "hk", "--to", "iast", test_input])
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_stdin_input():
    result = runner.invoke(
        app, ["--from", "hk", "--to", "iast", "--input-file", "-"], input=test_input
    )
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_file_input(tmp_path):
    test_input_file = tmp_path / "test_input_file.txt"
    test_input_file.write_text(test_input)

    result = runner.invoke(
        app, ["--from", "hk", "--to", "iast", "--input-file", test_input_file]
    )
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_file_output(tmp_path):
    test_output_file = tmp_path / "test_file_output.txt"

    result = runner.invoke(
        app,
        [
            "--from",
            "hk",
            "--to",
            "iast",
            "--output-file",
            test_output_file,
            test_input,
        ],
    )

    assert result.exit_code == 0
    assert f"Output written to: {test_output_file}" in result.stdout
    assert test_output_file.read_text() == expected_output
