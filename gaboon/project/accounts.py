from typing import List
from eth_account import Account as EthAccountClass
from eth_account.signers.local import (
    LocalAccount,
)


# TODO, this should probably be in its own folder/file
# TODO, same with networks
class Account(LocalAccount):
    name: str
    # TODO, make this locked and unlocked
    key: str | int

    def __init__(self, name: str, key: str | int):
        self.name = name
        self.key = key

    def __repr__(self):
        return f"Account('{self.name}')"


class Accounts(EthAccountClass):
    _accounts: List[Account]
    _name_map: dict

    def __init__(self):
        self._accounts = []
        self._name_map = {}

    def add(self, account):
        self._accounts.append(account)
        self._name_map[account.name] = account

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._accounts[key]
        elif isinstance(key, str):
            return self._name_map[key]
        else:
            raise TypeError("Key must be an integer or a string")

    def __setitem__(self, key: str, value: Account):
        if not isinstance(key, str):
            raise TypeError("Key must be a string when setting an item")
        if not isinstance(value, Account):
            raise TypeError("Value must be an Account object")
        if key != value.name:
            raise ValueError("Key must match the account name")

    def __len__(self):
        return len(self._accounts)

    def __iter__(self):
        return iter(self._accounts)

    def __repr__(self):
        return f"AccountContainer({self._accounts})"
