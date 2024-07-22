from pathlib import Path

from boa.contracts.vyper.vyper_contract import VyperDeployer

from gaboon.cli.compile import compile
from tests.base_test import COUNTER_PROJECT_FILE_PATH


def test_compile():
    result: VyperDeployer = compile(COUNTER_PROJECT_FILE_PATH, write_data=False)
    isinstance(result, VyperDeployer)
