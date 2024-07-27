from typing import List
import pytest
import os
import shutil
from gaboon.project import Project
from gaboon.project.gaboon_config import GaboonConfig
import json
import sys
from pathlib import Path

from .base_test import (
    COUNTER_PROJECT_PATH,
    MESC_CONFIG_PATH,
    ANVIL_SECOND_KEY,
    COMPLEX_NETWORKING_TOML,
)


@pytest.fixture
def cleanup_out_folder():
    yield
    created_folder_path = COUNTER_PROJECT_PATH.joinpath("out/")
    if os.path.exists(created_folder_path):
        shutil.rmtree(created_folder_path)


@pytest.fixture
def gaboon_project(cleanup_out_folder):
    return Project(COUNTER_PROJECT_PATH)


@pytest.fixture
def gaboon_config(cleanup_out_folder):
    return GaboonConfig(COUNTER_PROJECT_PATH)


@pytest.fixture
def mesc_config_json():
    with open(MESC_CONFIG_PATH, "r") as file:
        return json.load(file)


@pytest.fixture
def gab_path():
    return os.path.join(os.path.dirname(sys.executable), "gab")


@pytest.fixture
def complex_gab_config(monkeypatch):
    monkeypatch.setenv("GABOON_TEST_KEY", ANVIL_SECOND_KEY)
    config: GaboonConfig = GaboonConfig(COMPLEX_NETWORKING_TOML)
    yield config
    monkeypatch.delenv("GABOON_TEST_KEY")


@pytest.fixture
def all_commands():
    cli_dir = Path(__file__).parent.parent.joinpath("gaboon/cli")
    non_underscore_files: List[Path] = [
        file.stem for file in cli_dir.rglob("[!_]*.py") if file.is_file()
    ]
    return non_underscore_files
