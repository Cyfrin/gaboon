import json
from pathlib import Path
from typing import Any, List, Union
from eth_account import Account as EthAccountClass
from eth_account.signers.local import (
    LocalAccount,
)


class GaboonBaseAccount(EthAccountClass):
    address: str

    def __init__(self, address: str):
        self.address = address

    def __repr__(self):
        return f"BaseAccount('{self.address}')"

    def __hash__(self) -> int:
        return hash(self.address)

    def __str__(self) -> str:
        return self.address

    def __eq__(self, other: Union[object, str]) -> bool:
        if isinstance(other, str):
            return other == self.address
        if isinstance(other, GaboonBaseAccount):
            return other.address == self.address
        return super().__eq__(other)


class GaboonAccount(GaboonBaseAccount):
    keystore_path: Path
    password_file: Path

    def __init__(self, keystore_path: str):
        self.keystore_path = keystore_path
        self.password_file = None
        self.address = None


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
