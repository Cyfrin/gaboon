from pathlib import Path
from typing import Any
from types import ModuleType

from .gaboon_config import GaboonConfig
from gaboon.logging import logger
from gaboon.project.accounts import Account
from eth_account.signers.local import (
    LocalAccount,
)


class Project:
    # Attributes
    # ========================================================================
    root: Path
    config: GaboonConfig
    project_path: Path
    _boa: ModuleType | None

    # Constructors
    # ========================================================================
    def __init__(self, path: Path | str | None = None):
        self.root: Path = self.find_project_root(path or Path.cwd())
        self.config: GaboonConfig = self._load_config()
        self._boa: ModuleType | None = None

    # Special Methods
    # ========================================================================
    def __getattr__(self, name: str) -> Any:
        return getattr(self.config, name)

    # Public Methods
    # ========================================================================
    def set_boa_network_env(self, network_url: str | None = None):
        if self.boa.env.eoa is not None:
            logger.warning("Resestting boa ENV, all boa state will be reset")
        if network_url is None:
            network_url = self.networks.active_network.url
        logger.debug(f"Setting boa network env to {self.networks.active_network.url}")
        self.boa.set_network_env(network_url)
        self.set_boa_eoa()

    def set_boa_eoa(self, eoa: Account | None = None):
        if not eoa:
            eoa: Account = self.default_account
        if not eoa.unlocked:
            eoa.prompt_for_unlock()
        formatted_account: LocalAccount = Account.from_key(eoa.private_key)
        self.boa.env.set_eoa(formatted_account)
        logger.info(f"Set boa EOA to {formatted_account.address}")

    # Internal Methods
    # ========================================================================
    def _load_config(self) -> GaboonConfig:
        return GaboonConfig(self.root)

    # Static Methods
    # ========================================================================
    @staticmethod
    def find_project_root(start_path: Path | str = Path.cwd()) -> Path:
        current_path = Path(start_path).resolve()
        while True:
            if (current_path / "gaboon.toml").exists():
                return current_path

            # Check for src directory with .vy files in current directory
            src_path = current_path / "src"
            if src_path.is_dir() and any(src_path.glob("*.vy")):
                return current_path

            # Check for gaboon.toml in parent directory
            if (current_path.parent / "gaboon.toml").exists():
                return current_path.parent

            # Move up to the parent directory
            parent_path = current_path.parent
            if parent_path == current_path:
                # We've reached the root directory without finding gaboon.toml
                raise FileNotFoundError(
                    "Could not find gaboon.toml or src directory with Vyper contracts in any parent directory"
                )
            current_path = parent_path

    # Properties
    # ========================================================================
    @property
    def boa(self) -> ModuleType:
        if self._boa is None:
            if self._boa is None:
                import boa

                self._boa = boa
                self._boa.env = self._boa.Env()
                logger.debug(
                    f"Project {id(self)}: Imported boa, env id: {id(self._boa.env)}"
                )
            else:
                logger.debug(
                    f"Project {id(self)}: Using existing boa, env id: {id(self._boa.env)}"
                )
        return self._boa
