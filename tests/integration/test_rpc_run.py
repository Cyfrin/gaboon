import pytest
from tests.utils.anvil import AnvilProcess
from tests.base_test import COUNTER_PROJECT_PATH, COUNTER_PROJECT_FILE_PATH
from gaboon.project.project_class import Project
from gaboon.cli.run import run_script_by_project
from eth_account import Account


# This will skip all the tests in here.
pytestmark = pytest.mark.integration

ANVIL_NETWORK = {"url": "http://127.0.0.1:8545", "name": "anvil", "chain_id": 1337}
ANVIL_DEFAULT_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"


def test_deploy_to_anvil():
    my_project: Project = Project(COUNTER_PROJECT_PATH)
    my_project.networks.add_network(ANVIL_NETWORK)
    my_project.networks.set_active_network("anvil")
    my_account: Account = Account.from_key(ANVIL_DEFAULT_KEY)
    my_project.boa.add_account(my_account)

    with AnvilProcess():
        # This should deploy the contract to our chain
        run_script_by_project(my_project, "deploy")
        counter_factory = my_project.boa.load(COUNTER_PROJECT_FILE_PATH)
