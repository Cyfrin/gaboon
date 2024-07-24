import subprocess
from pathlib import Path
from tests.base_test import COMPLEX_NETWORKING_PROJECT_PATH
import os

EXPECTED_HELP_TEXT = "Runs a script"


# def test_run_gaboon_project(gab_path):
#     current_dir = Path.cwd()
#     try:
#         os.chdir(COMPLEX_NETWORKING_PROJECT_PATH)
#         result = subprocess.run(
#             [gab_path, "run", "deploy"],
#             capture_output=True,
#             text=True,
#             check=True,
#         )
#         assert "Running run command" in result.stderr
#         assert result.returncode == 0
#     finally:
#         os.chdir(current_dir)
