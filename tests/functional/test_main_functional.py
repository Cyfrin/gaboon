import subprocess

EXPECTED_HELP_TEXT = "Pythonic Smart Contract Development Framework"


def test_help(gab_path):
    result = subprocess.run(
        [gab_path, "-h"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        EXPECTED_HELP_TEXT in result.stdout
    ), "Help output does not contain expected text"
    assert result.returncode == 0
