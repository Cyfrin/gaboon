from gaboon.cli.run import get_script_path


def test_run(gaboon_project):
    script_path = get_script_path(gaboon_project, "deploy")
    assert script_path == gaboon_project.root / gaboon_project.script / "deploy.py"
