from gaboon.project.networks import Network


def test_network_is_just_a_dict(gaboon_config):
    isinstance(gaboon_config.networks, Network)
    isinstance(gaboon_config.networks, dict)
