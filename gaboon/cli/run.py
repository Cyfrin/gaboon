from typing import List, Any
import sys
from pathlib import Path
from gaboon.project.project_class import Project
import importlib.util
from gaboon.logging import logger


def main(args: List[Any]) -> int:
    run_script(args.project_root, args.script_name_or_path)
    return 0


def run_script(root: Path | str, script_name_or_path: Path | str):
    project = Project(root)
    run_script_by_project(project, script_name_or_path, root)


def run_script_by_project(
    project: Project, script_name_or_path: Path | str, root: Path | str | None = None
):
    if root is None:
        root = project.root
    script_path: Path = get_script_path(project, script_name_or_path)

    # Set up the environment (add necessary paths to sys.path, etc.)
    sys.path.insert(0, str(root)) if root not in sys.path else None
    sys.path.insert(0, str(root / project.src)) if (
        root / project.src
    ) not in sys.path else None

    # We give the user's script the module name "deploy_script"
    spec = importlib.util.spec_from_file_location("deploy_script", script_path)
    if spec is None:
        logger.error(f"Cannot find module spec for '{script_path}'")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        logger.error(f"Cannot find loader for '{script_path}'")
        sys.exit(1)

    if project.active_network.url != "" and project.active_network.url is not None:
        project.set_boa_network_env()
    module.__dict__["boa"] = project.boa
    spec.loader.exec_module(module)

    if hasattr(module, "main") and callable(module.main):
        module.main()
    else:
        logger.info("No main() function found. Executing script as is...")
    sys.path.pop(0)
    sys.path.pop(0)


def get_script_path(project: Project, script_name_or_path: Path | str) -> Path:
    script_path = Path(script_name_or_path)

    if script_path.suffix != ".py":
        script_path = script_path.with_suffix(".py")

    if not script_path.is_absolute():
        if project.script not in script_path.parts:
            script_path = project.root / project.script / script_path
        else:
            script_path = project.root / script_path

    if not script_path.exists():
        logger.error(f"{script_path} not found")

    return script_path
