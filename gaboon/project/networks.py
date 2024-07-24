from typing import Any, Dict, Optional, Union
from gaboon.logging import logger
from eth_account import Account


DEFAULT_NETWORK_NAME = "default_network"
DEVELOPMENT_NETWORK_NAME = "development"
ENDPOINTS_CONFIG_NAME = "networks"

DEVELOPMENT_NETWORK_DICT = {
    DEVELOPMENT_NETWORK_NAME: {
        "url": "",
        "chain_id": 1337,
        "default_account": "anvil_key",
        "name": DEVELOPMENT_NETWORK_NAME,
    }
}


class Network:
    name: str
    default_account: Account
    accounts: Dict[str, Account]

    def __init__(self, network_data: dict):
        for key, value in network_data.items():
            setattr(self, key, value)

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


class Networks:
    _networks: Dict[str, Network]
    active_network_name: str

    def __init__(
        self, networks: Dict[str, dict], active_network_name: str | None = None
    ):
        self._networks = {}
        for network_name, network_data in networks.items():
            self._networks[network_name] = Network(network_data)

        if DEVELOPMENT_NETWORK_NAME not in self._networks:
            self.update(DEVELOPMENT_NETWORK_DICT)

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

    def get(self, key, default=None):
        return self._networks.get(key, default)

    def update(self, other: Dict[str, dict]):
        for key, value in other.items():
            self[key] = value

    def set_active_network(self, active_network_name: str | None):
        if active_network_name is None:
            active_network_name = DEVELOPMENT_NETWORK_NAME
        self.active_network_name: str = active_network_name

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

    @property
    def networks(self) -> Dict[str, Network]:
        return self._networks

    @property
    def active_network(self) -> Network:
        return self._networks[self.active_network_name]
