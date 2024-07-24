import subprocess
import tempfile
from pathlib import Path
from gaboon.project.project_class import Project

from tests.base_test import assert_files_and_folders_exist

EXPECTED_HELP_TEXT = "Pythonic Smart Contract Development Framework"


def test_init(gab_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        result = subprocess.run(
            [gab_path, "init", Path(temp_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert_files_and_folders_exist(Path(temp_dir))
        assert_files_and_folders_exist(Path(temp_dir))
        assert result.returncode == 0


def test_find_project_root_from_new_project(gab_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        result = subprocess.run(
            [gab_path, "init", Path(temp_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
        project_root: Path = Project.find_project_root(Path(temp_dir))
        assert project_root.resolve() == Path(temp_dir).resolve()
        assert result.returncode == 0
