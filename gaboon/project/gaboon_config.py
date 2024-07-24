import os
import tomllib
from pathlib import Path
from typing import Any, Optional, Union
import json
from gaboon.logging import logger
from gaboon.project.networks import (
    Network,
    Networks,
    DEFAULT_NETWORK_NAME,
    DEVELOPMENT_NETWORK_NAME,
    ENDPOINTS_CONFIG_NAME,
    DEVELOPMENT_NETWORK_DICT,
)

DEFAULT_VYPER_VERSION = "0.4.0"

GABOON_DEFAULT_CONFIG = {
    "profile": {
        "default": {
            "src": "src",
            "test": "tests",
            "script": "script",
            "out": "out",
            "libs": ["lib"],
            "remappings": [],
            "mesc_path": "",
            DEFAULT_NETWORK_NAME: DEVELOPMENT_NETWORK_NAME,
        }
    },
    ENDPOINTS_CONFIG_NAME: DEVELOPMENT_NETWORK_DICT,
}

GABOON_PROFILE_ENV_VAR = "GABOON_PROFILE"
FOUNDRY_PROFILE_ENV_VAR = "FOUNDRY_PROFILE"
DEFAULT_PROFILE_NAME = "default"


class GaboonConfig:
    # Attributes
    # ========================================================================
    active_profile: str | None
    config_data: dict
    networks: Networks

    # Constructors
    # ========================================================================
    def __init__(
        self, config_source: Union[dict, Path] | None, active_profile: str | None = None
    ):
        if isinstance(config_source, dict):
            self.set_config_data(config_source, active_profile)
        elif isinstance(config_source, Path):
            self._init_from_path(config_source)
        elif config_source is None:
            self.set_config_data(GABOON_DEFAULT_CONFIG)

    def _init_from_path(self, config_path: Path):
        config_data = self.read_gaboon_config(config_path)
        self.set_config_data(config_data)

    # Special Methods
    # ========================================================================
    def __getattr__(self, name: str) -> Any:
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.active_profile_data:
            return self.active_profile_data[name]
        if name in self.config_data:
            return self.config_data[name]
        return getattr(self.config_data, name)

    def __repr__(self):
        return f"GaboonConfig({self.active_profile_data})"

    def __str__(self):
        return self.__repr__()

    # Public Methods
    # ========================================================================
    def set_config_data(self, config_data: dict, active_profile: str | None = None):
        if active_profile is None:
            active_profile = os.getenv(GABOON_PROFILE_ENV_VAR) or os.getenv(
                FOUNDRY_PROFILE_ENV_VAR
            )
            if active_profile:
                self.active_profile = active_profile
            else:
                self.active_profile = DEFAULT_PROFILE_NAME
        self.config_data = config_data
        self.add_mesc_endpoints_to_config(
            self.active_profile_data.get("mesc_path", None)
        )
        self._load_networks()

    def add_mesc_endpoints_to_config(
        self, mesc_path: Optional[Path] = None, load_networks_after: bool = True
    ):
        """
        Adds endpoints using the MESC format.
        https://github.com/paradigmxyz/mesc

        Args:
            mesc_path: The path of the `mesc.json` file. If None, defaults to ~/mesc.json.
            load_networks_after: Whether to load the networks after adding the endpoints.

        Returns:
            bool: True if endpoints were successfully added, False otherwise.
        """
        if mesc_path is None:
            mesc_path = Path.home() / "mesc.json"

        if not mesc_path.exists():
            logger.warning(f"MESC file not found at {mesc_path}, nothing loaded")
            return

        with mesc_path.open("r") as file:
            mesc_data = json.load(file)
            endpoints = mesc_data.get("endpoints", {})

            if ENDPOINTS_CONFIG_NAME not in self.config_data:
                self.config_data[ENDPOINTS_CONFIG_NAME] = {}
            self.config_data[ENDPOINTS_CONFIG_NAME].update(endpoints)
        logger.info(f"Successfully added MESC endpoints from {mesc_path}")

        if load_networks_after:
            self._load_networks()

    def change_profile(self, new_profile: str):
        self.set_active_profile(new_profile)

    def set_active_profile(self, active_profile: str):
        self.active_profile = active_profile
        self.active_profile_data = self.config_data["profile"][active_profile]
        self.networks.set_active_network(
            self.config_data["profile"][active_profile][DEFAULT_NETWORK_NAME]
        )

    def read_gaboon_config(self, config_path: Path) -> dict:
        if not str(config_path).endswith("/gaboon.toml"):
            config_path = config_path.joinpath("gaboon.toml")
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, "rb") as f:
            return tomllib.load(f)

    # Internal Methods
    # ========================================================================
    def _load_networks(self):
        if self.config_data.get(ENDPOINTS_CONFIG_NAME, None) is None:
            self.config_data[ENDPOINTS_CONFIG_NAME] = DEVELOPMENT_NETWORK_DICT
        self.networks = Networks(self.config_data[ENDPOINTS_CONFIG_NAME])

    # Properties
    # ========================================================================
    @property
    def active_network(self) -> Network:
        return self.networks.active_network

    @property
    def active_profile_data(self) -> dict:
        return self.config_data["profile"][self.active_profile]
