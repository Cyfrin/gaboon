from pathlib import Path
from gaboon.utils._cli_constants import (
    GITATTRIBUTES,
    GITIGNORE,
    PROJECT_FOLDERS,
)

ANVIL_NETWORK = {"url": "http://127.0.0.1:8545", "name": "anvil", "chain_id": 1337}
ANVIL_DEFAULT_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
ANVIL_SECOND_KEY = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

COMPLEX_NETWORKING_TOML = Path(__file__).parent.joinpath(
    "data/test_configs/complex_networking/gaboon.toml"
)

COMPLEX_NETWORKING_PROJECT_PATH = Path(__file__).parent.joinpath(
    "data/test_projects/gaboon_networking_monstrosity"
)

COUNTER_PROJECT_PATH = Path(__file__).parent.joinpath(
    "data/test_projects/gaboon_project"
)
COUNTER_PROJECT_FILE_PATH = COUNTER_PROJECT_PATH.joinpath("src/Counter.vy")
MESC_CONFIG_PATH = Path(__file__).parent.joinpath("data/test_configs/test_mesc.json")


def assert_files_and_folders_exist(temp_dir: Path):
    for folder in PROJECT_FOLDERS:
        assert temp_dir.joinpath(folder).exists()
    assert temp_dir.joinpath("README.md").exists()
    assert temp_dir.joinpath("gaboon.toml").exists()
    # assert the temp_dir dir has the .gitignore and .gitattributes
    assert temp_dir.joinpath(Path(".gitignore")).exists()
    assert temp_dir.joinpath(Path(".gitattributes")).exists()
    # assert the content of the .gitignore and .gitattributes
    with temp_dir.joinpath(Path(".gitignore")).open() as fp:
        assert fp.read() == GITIGNORE
    with temp_dir.joinpath(Path(".gitattributes")).open() as fp:
        assert fp.read() == GITATTRIBUTES
