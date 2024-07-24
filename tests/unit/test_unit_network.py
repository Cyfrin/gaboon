from gaboon.project.networks import Networks


def test_network_is_just_a_dict(gaboon_config):
    isinstance(gaboon_config.networks, Networks)
    isinstance(gaboon_config.networks, dict)
