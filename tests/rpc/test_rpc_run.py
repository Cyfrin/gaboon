from typing import Any
import pytest
from tests.utils.anvil import AnvilProcess
from tests.base_test import (
    COUNTER_PROJECT_PATH,
    COUNTER_PROJECT_FILE_PATH,
    ANVIL_NETWORK,
    ANVIL_DEFAULT_KEY,
    ANVIL_SECOND_KEY,
)
from gaboon.project.project_class import Project
from gaboon.cli.run import run_script_by_project
from gaboon.project.accounts import Accounts, Account


# This will skip all the tests in here.
pytestmark = pytest.mark.integration


def test_deploy_to_anvil():
    my_project: Project = Project(COUNTER_PROJECT_PATH)
    my_project.networks.add_network(ANVIL_NETWORK)
    my_project.networks.set_active_network("anvil")

    with AnvilProcess():
        my_project.set_boa_network_env(ANVIL_NETWORK["url"])
        my_account: Account = Accounts.from_key(ANVIL_DEFAULT_KEY)
        my_project.boa.env.set_eoa(my_account)
        result_contract: Any | None = run_script_by_project(my_project, "deploy")
        if result_contract:
            assert result_contract.number() == 1
        else:
            assert False
