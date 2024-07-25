from gaboon.cli.wallet import list_accounts
from pathlib import Path

TEST_KEYSTORES_PATH: Path = Path(__file__).parent.parent.joinpath(
    "data/test_keystores/keystores"
)


def test_list_wallets():
    result = list_accounts(TEST_KEYSTORES_PATH)
    assert "anvil" in result[0].stem
