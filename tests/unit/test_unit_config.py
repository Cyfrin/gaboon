from tests.base_test import MESC_CONFIG_PATH


def test_add_mesc_endpoints_to_config(gaboon_config, mesc_config_json):
    gaboon_config.add_mesc_endpoints_to_config(MESC_CONFIG_PATH)
    del gaboon_config.networks["development"]
    assert mesc_config_json["endpoints"] == gaboon_config.networks
