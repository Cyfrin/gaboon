import os
import subprocess
from pathlib import Path

from tests.conftest import COMPLEX_PROJECT_PATH


# --------------------------------------------------------------
#                         WITHOUT ANVIL
# --------------------------------------------------------------
def test_deploy_price_feed_pyevm(mox_path, complex_project_config):
    current_dir = Path.cwd()
    try:
        os.chdir(COMPLEX_PROJECT_PATH)
        result = subprocess.run(
            [mox_path, "deploy", "price_feed"],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        os.chdir(current_dir)
    assert "Deployed contract price_feed on pyevm to" in result.stderr


# --------------------------------------------------------------
#                           WITH ANVIL
# --------------------------------------------------------------
def test_deploy_price_feed_anvil(mox_path, anvil_process):
    current_dir = Path.cwd()
    try:
        os.chdir(COMPLEX_PROJECT_PATH)
        result = subprocess.run(
            [mox_path, "deploy", "price_feed", "--network", "anvil"],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        os.chdir(current_dir)
    assert "Deployed contract price_feed on anvil to" in result.stderr
