from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from gaboon.logging import logger
from .accounts import Accounts, Account
from gaboon.cli.wallet import list_accounts
from boa.rpc import EthereumRPC


DEFAULT_NETWORK_NAME = "default_network"
DEVELOPMENT_NETWORK_NAME = "development"
DEVELOPMENT_NETWORK_NAMES = [DEVELOPMENT_NETWORK_NAME, "dev"]
ENDPOINTS_CONFIG_NAME = "networks"

DEVELOPMENT_NETWORK_DICT = {
    DEVELOPMENT_NETWORK_NAME: {
        "url": "",
        "chain_id": 1337,
        "default_account_name": "anvil1",
        "name": DEVELOPMENT_NETWORK_NAME,
    }
}


class Network:
    name: str
    accounts: Accounts
    default_account_name: str
    rpc: EthereumRPC | None

    def __init__(
        self,
        network_data: dict,
        default_account_name: str | None = None,
        rpc: str | EthereumRPC | None = None,
    ):
        self.name = ""
        self.accounts = Accounts()
        self.default_account_name = ""
        for key, value in network_data.items():
            if key == "default_account_name":
                self.default_account_name = value
            else:
                setattr(self, key, value)
        if isinstance(rpc, EthereumRPC):
            self.rpc = rpc
        if isinstance(rpc, str):
            self.rpc = EthereumRPC(rpc)
        self.default_account_name = default_account_name

    def __repr__(self):
        return f"Network({self.__dict__})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.__dict__ == other
        if isinstance(other, Network):
            return self.__dict__ == other.__dict__
        return False

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __contains__(self, key):
        return hasattr(self, key)

    def __getattr__(self, name: str) -> Any:
        if name in self.accounts:
            return self.accounts[name]

    def get(self, key, default=None):
        return getattr(self, key, default)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    @property
    def default_account(self) -> Account | None:
        if self.default_account_name is not None:
            return self.accounts[self.default_account_name]
        elif len(self.accounts) > 0:
            return self.accounts[0]
        else:
            return None

    @property
    def url(self) -> str:
        return self.rpc.identifier


class Networks:
    _networks: Dict[str, Network]
    active_network_name: str | None
    global_default_account_name: str | None
    _global_unsafe_keys: Accounts | None
    accounts: Accounts

    def __init__(
        self,
        networks: Dict[str, dict],
        active_network_name: str | None = None,
        global_default_account_name: str | None = None,
        global_unsafe_keys: Accounts | List[str] | None = None,
    ):
        self.global_default_account_name = global_default_account_name
        self.active_network_name = active_network_name
        if isinstance(global_unsafe_keys, List):
            global_unsafe_keys = Accounts(
                unsafe_keys=global_unsafe_keys,
                default_account_name=global_default_account_name,
            )
        self._global_unsafe_keys = global_unsafe_keys
        self._networks = {}
        for network_name, network_data in networks.items():
            logger.debug(f"Initializing network {network_name}.")
            self._networks[network_name] = Network(network_data)
        if DEVELOPMENT_NETWORK_NAME not in self._networks:
            self.update(DEVELOPMENT_NETWORK_DICT)

        account_paths: List[Path] = list_accounts()
        self.accounts = Accounts()
        self.accounts.append(self._global_unsafe_keys)
        for account_path in account_paths:
            account_name = account_path.stem
            account = Account(name=account_name)
            self.accounts.add(account)

        self.set_active_network(active_network_name)

    def __getitem__(self, key: str) -> Network:
        return self._networks[key]

    def __setitem__(self, key: str, value: dict):
        self._networks[key] = Network(value)

    def __contains__(self, key: str) -> bool:
        return key in self._networks

    def __iter__(self):
        return iter(self._networks)

    def __len__(self):
        return len(self._networks)

    def __repr__(self):
        return f"Networks({self._networks})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, Networks):
            return (
                self._networks == other._networks
                and self.active_network_name == other.active_network_name
            )
        elif isinstance(other, dict):
            # we ignore active_network_name for dicts... for now?
            return self._networks == other
        return False

    def __delitem__(self, key: str):
        if key in self._networks:
            del self._networks[key]
        else:
            raise KeyError(key)

    def __getattr__(self, name: str) -> Network:
        if name in self._networks:
            return self._networks[name]
        if name in self.__class__.__dict__:
            return getattr(self.__class__, name)
        raise AttributeError(f"'Networks' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Union[Network, dict, Accounts, None]):
        if name in [
            "_networks",
            "active_network_name",
            "_global_unsafe_keys",
            "global_default_account_name",
        ]:
            super().__setattr__(name, value)
        else:
            if isinstance(value, Network):
                self._networks[name] = value
            elif isinstance(value, Accounts):
                self._networks[name] = value
            elif isinstance(value, dict):
                self._networks[name] = Network(value)
            else:
                raise ValueError(
                    "Network must be a Network object, Accounts object, None, or a dict."
                )

    def __delattr__(self, name: str):
        if name in self._networks:
            del self._networks[name]
        else:
            raise AttributeError(f"'Networks' object has no attribute '{name}'")

    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        return self._networks.get(key, default)

    def update(self, other: Dict[str, dict]):
        for key, value in other.items():
            self[key] = value

    def set_active_network(
        self, active_network_name_or_url_or_network: str | Network | None
    ):
        if isinstance(active_network_name_or_url_or_network, Network):
            self.active_network_name: str = active_network_name_or_url_or_network.name
        elif isinstance(active_network_name_or_url_or_network, str):
            if self.is_valid_rpc(active_network_name_or_url_or_network):
                if active_network_name_or_url_or_network not in self._networks:
                    self.add_network(active_network_name_or_url_or_network)
        # if active_network_name_or_url_or_network in DEVELOPMENT_NETWORK_NAMES:
        #     active_network_name_or_url = DEVELOPMENT_NETWORK_NAME
        # if active_network_name_or_url_or_network is None:
        #     active_network_name_or_url = DEVELOPMENT_NETWORK_NAME
        # if active_network_name_or_url_or_network not in self._networks:
        #     if self.is_valid_rpc():
        #         self.add_network(
        #             active_network_name_or_url,
        #             active_network_name_or_url,
        #         )
        #     else:
        #         logger.error(
        #             f"Network {active_network_name_or_url} not found in networks, or is not a valid RPC."
        #         )
        # if self.active_network_name != active_network_name_or_url:
        #     logger.debug(f"Changed active network to {active_network_name_or_url}.")
        #     self.active_network_name: str = active_network_name_or_url

    def add_network(
        self,
        network: Union[Network, str],
        url: Optional[str] = None,
        chain_id: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Add a network to the Networks object.

        :param network: Either a Network object or the name of the network.
        :param url: The URL of the network (required if network is a string).
        :param chain_id: The chain ID of the network (optional).
        :param kwargs: Additional keyword arguments for network properties.
        """
        if isinstance(network, dict):
            network = Network(network)
        if isinstance(network, Network):
            self._networks[network.name] = network
            logger.debug(
                f"Added network {network.name} from Network object to networks."
            )
        elif isinstance(network, str):
            if url is None:
                raise ValueError("URL must be provided when adding a network by name.")
            network_data = {"name": network, "url": url}
            if chain_id is not None:
                network_data["chain_id"] = chain_id
            network_data.update(kwargs)
            new_network = Network(**network_data)
            self._networks[network] = new_network
            logger.debug(f"Added network {network.name} from dict object to networks.")
        else:
            raise ValueError(
                "Network must be a Network object, dict, or a set of strings."
            )

    def get_network_urls(self) -> List[str]:
        return [network.url for network in self._networks.values()]

    @property
    def networks(self) -> Dict[str, Network]:
        return self._networks

    @property
    def active_network(self) -> Network:
        return self._networks[self.active_network_name]

    @active_network.setter
    def active_network(self, value):
        self.set_active_network(value)

    @property
    def accounts(self) -> Accounts:
        for network in self._networks.values():
            if network.default_account_name is not None:
                return network.accounts

    @property
    def default_account(self) -> Account | None:
        if self.active_network.default_account is not None:
            return self.active_network.default_account
        elif self.global_default_account_name is not None:
            return self.accounts[self.global_default_account_name]
        else:
            return None

    @classmethod
    def is_valid_rpc(cls, url: str) -> bool:
        return url.startswith("http")
