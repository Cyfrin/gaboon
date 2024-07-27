import subprocess

EXPECTED_HELP_TEXT = "Pythonic Smart Contract Development Framework"


def test_help_and_debug_all_comamnds(gab_path, all_commands):
    for command in all_commands:
        result = subprocess.run(
            [gab_path, command, "-h", "--debug"],
            check=True,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
