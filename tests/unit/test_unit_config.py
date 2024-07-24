from tests.base_test import MESC_CONFIG_PATH, COMPLEX_NETWORKING_TOML, ANVIL_SECOND_KEY
from gaboon.project.gaboon_config import GaboonConfig
import os


def test_add_mesc_endpoints_to_config(gaboon_config, mesc_config_json):
    gaboon_config.add_mesc_endpoints_to_config(MESC_CONFIG_PATH)
    del gaboon_config.networks["development"]
    assert mesc_config_json["endpoints"] == gaboon_config.networks


def test_initialize_config_sets_default_network(complex_gab_config):
    assert complex_gab_config.networks.active_network.name == "fake_sepolia"


def test_initialize_config_sets_default_account(complex_gab_config):
    assert complex_gab_config.networks.default_account == "my_account"


def test_initialize_config_sets_number_of_accounts(complex_gab_config):
    assert len(complex_gab_config.networks.fake_zksync.accounts) == 3


def test_initialize_config_converts_private_key_to_account(complex_gab_config):
    # assert complex_gab_config.networks.fake_zksync.accounts[0]
    pass
