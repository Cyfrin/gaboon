def test_config_attributes_exposed_in_project(gaboon_config, gaboon_project):
    for attr in dir(gaboon_config):
        if not attr.startswith("__") and not callable(getattr(gaboon_config, attr)):
            assert hasattr(
                gaboon_project, attr
            ), f"Project is missing attribute: {attr}"
            config_value = getattr(gaboon_config, attr)
            project_value = getattr(gaboon_project, attr)

            if isinstance(config_value, dict):
                assert (
                    config_value == project_value
                ), f"Mismatch in dict attribute: {attr}"
            elif isinstance(config_value, (list, tuple, set)):
                assert set(config_value) == set(
                    project_value
                ), f"Mismatch in iterable attribute: {attr}"
            else:
                assert config_value == project_value, f"Mismatch in attribute: {attr}"
