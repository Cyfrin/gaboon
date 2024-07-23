import subprocess
import os
from tests.base_test import COUNTER_PROJECT_PATH
from pathlib import Path

EXPECTED_HELP_TEXT = "Vyper compiler"


def test_compile_help():
    result = subprocess.run(
        ["gab", "compile", "-h"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        EXPECTED_HELP_TEXT in result.stdout
    ), "Help output does not contain expected text"
    assert result.returncode == 0


def test_build_help():
    result = subprocess.run(
        ["gab", "build", "-h"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        EXPECTED_HELP_TEXT in result.stdout
    ), "Help output does not contain expected text"
    assert result.returncode == 0


def test_compile_alias_build_project(cleanup_out_folder):
    current_dir = Path.cwd()
    try:
        os.chdir(COUNTER_PROJECT_PATH)
        result = subprocess.run(
            ["gab", "build"],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "Running compile command" in result.stderr
        assert result.returncode == 0
    finally:
        os.chdir(current_dir)
    assert result.returncode == 0
