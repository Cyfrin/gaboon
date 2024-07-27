from getpass import getpass
import json
from pathlib import Path
from typing import Any, List, Union
from eth_account import Account as EthAccountClass
from eth_account.signers.local import (
    LocalAccount,
)
from gaboon.utils._cli_constants import DEFAULT_KEYSTORES_PATH

PASSWORD_RETRIES: int = 3


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


class Account(GaboonBaseAccount):
    name: str
    private_key: str | None
    address: str | None
    keystore_path: Path | None

    def __init__(
        self,
        private_key: str | None = None,
        name: str | None = None,
        keystore_path: str | Path = DEFAULT_KEYSTORES_PATH,
    ):
        self.name = name
        self.keystore_path = keystore_path
        self.private_key = private_key
        self.address = None
        if self.name is None:
            if not private_key:
                raise ValueError("Name or unsafe private key must be provided")
            self.name = "unsafe_key"

    def prompt_for_unlock(self):
        prompt = f'Enter password for "{self.name}": '
        retries = 0
        while True:
            password = getpass(prompt)
            keystore_file_path = Path(self.keystore_path).joinpath(self.name)
            with open(keystore_file_path, "r") as keyfile:
                keyfile_json = json.loads(keyfile.read())
            try:
                priv_key = self.decrypt(keyfile_json, password)
                break
            except ValueError as e:
                if retries < PASSWORD_RETRIES:
                    prompt = f"Incorrect password, {retries} tries left:"
                    password = None
                    retries += 1
                    continue
                raise e
        self.private_key = priv_key

    @property
    def unlocked(self):
        return self.private_key is not None


class Accounts(EthAccountClass):
    _accounts: List[Account]
    _name_map: dict[str, Account]
    _default_account_name: str | None
    _unsafe_key_counter: int

    def __init__(
        self,
        unsafe_keys: Union[List[str] | "Accounts"] = None,
        default_account_name: str | None = None,
    ):
        self._accounts = []
        self._name_map = {}
        self._unsafe_key_counter = 0
        self._default_account_name = default_account_name
        if unsafe_keys is not None and len(unsafe_keys) > 0:
            if isinstance(unsafe_keys, List) and isinstance(unsafe_keys[0], str):
                for unsafe_key in unsafe_keys:
                    unsafe_key_account: Account = Account(
                        private_key=unsafe_key,
                        name=f"unsafe_key_{self._unsafe_key_counter}",
                    )
                    self.add(unsafe_key_account)
            else:
                self.append(unsafe_keys)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, dict):
            return self._name_map == other
        if len(self._accounts) != len(other._accounts):
            return False
        if not isinstance(other, Accounts):
            return NotImplemented
        if self._name_map != other._name_map:
            return False
        return True

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
        return f"Accounts({self._accounts})"

    def add(self, account: Account | str):
        if isinstance(account, str):
            account = Account(account)
        self._accounts.append(account)
        self._name_map[account.name] = account

    def append(self, accounts: "Accounts"):
        for account in accounts:
            self.add(account)

    @property
    def default_account(self) -> Account:
        if self._default_account_name is None:
            if self.len() == 0:
                raise ValueError("No accounts available")
            return self.len()
        return self._name_map[self._default_account_name]
