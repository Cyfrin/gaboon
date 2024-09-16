from pathlib import Path
from moccasin.logging import logger
from moccasin.constants.vars import (
    CONFIG_NAME,
    DEFAULT_PROJECT_FOLDERS,
    README_PATH,
    COUNTER_CONTRACT,
    CONTRACTS_FOLDER,
    SCRIPT_FOLDER,
    TESTS_FOLDER,
)
from moccasin.constants.file_data import (
    GITIGNORE,
    GITATTRIBUTES,
    README_MD_SRC,
    COUNTER_VYPER_CONTRACT_SRC,
    CONFTEST_DEFAULT,
    COVERAGERC,
    DEPLOY_SCRIPT_DEFAULT,
    TEST_COUNTER_DEFAULT,
    GAB_DEFAULT_CONFIG,
    VSCODE_SETTINGS_DEFAULT,
)
from argparse import Namespace


def main(args: Namespace) -> int:
    path: Path = new_project(
        args.path or ".", args.force or False, args.vscode or False
    )
    logger.info(f"Project initialized at {str(path)}")
    return 0


def new_project(
    project_path_str: str = ".", force: bool = False, vscode: bool = False
) -> Path:
    """Initializes a new project.

    Args:
        project_path: Path to initialize the project at. If not exists, it will be created.
        force: If True, it will create folders and files even if the folder is not empty.
        vscode: If True, it will create a .vscode folder with settings.json

    Returns the path to the project as a string.
    """
    project_path = Path(project_path_str).resolve()
    if not force and project_path.exists() and list(project_path.glob("*")):
        raise FileExistsError(
            f"Directory is not empty: {project_path}.\nIf you're sure the folder is ok to potentially overwrite, try creating a new project by running with `mox init --force`"
        )
    project_path.mkdir(exist_ok=True)
    _create_folders(project_path, vscode=vscode)
    _create_files(project_path, vscode=vscode)
    return project_path


def _create_folders(project_path: Path, vscode: bool = False) -> None:
    for folder in DEFAULT_PROJECT_FOLDERS:
        Path(project_path).joinpath(folder).mkdir(exist_ok=True)
    if vscode:
        Path(project_path).joinpath(".vscode").mkdir(exist_ok=True)


def _create_files(project_path: Path, vscode: bool = False) -> None:
    _write_file(project_path.joinpath(".gitignore"), GITIGNORE)
    _write_file(project_path.joinpath(".gitattributes"), GITATTRIBUTES)
    _write_file(project_path.joinpath(".coveragerc"), COVERAGERC)
    _write_file(
        project_path.joinpath(f"{CONTRACTS_FOLDER}/{COUNTER_CONTRACT}"),
        COUNTER_VYPER_CONTRACT_SRC,
    )
    _write_file(project_path.joinpath(CONFIG_NAME), GAB_DEFAULT_CONFIG)
    _write_file(project_path.joinpath(README_PATH), README_MD_SRC)
    _write_file(project_path.joinpath(f"{TESTS_FOLDER}/conftest.py"), CONFTEST_DEFAULT)
    _write_file(
        project_path.joinpath(f"{TESTS_FOLDER}/test_counter.py"), TEST_COUNTER_DEFAULT
    )
    _write_file(
        project_path.joinpath(f"{SCRIPT_FOLDER}/deploy.py"), DEPLOY_SCRIPT_DEFAULT
    )
    _write_file(project_path.joinpath(f"{SCRIPT_FOLDER}/__init__.py"), "")
    if vscode:
        _write_file(
            project_path.joinpath(".vscode/settings.json"), VSCODE_SETTINGS_DEFAULT
        )


def _write_file(path: Path, contents: str, overwrite: bool = False) -> None:
    if not path.exists() or overwrite:
        with path.open("w") as fp:
            fp.write(contents)
