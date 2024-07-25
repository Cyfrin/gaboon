"""
Wallet management utilities

Usage: gab wallet <COMMAND>

Commands:
  list              List all the accounts in the keystore default directory [aliases: ls]
  generate          Add a new account with a random private key [aliases: g]
  address           Convert a private key to an address [aliases: a, addr]
  sign              Sign a message or typed data [aliases: s]
  verify            Verify the signature of a message [aliases: v]
  import            Import a private key into an encrypted keystore [aliases: i]
  export            Export an existing account keystore file [aliases: e]
  password          Change the password of an existing account
  private-key       Derives private key from mnemonic [aliases: pk]
  decrypt-keystore  Decrypt a keystore file to get the private key [aliases: dk]
  help              Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
"""

import json
from pathlib import Path
from typing import Any, List
from gaboon.project import Project
from gaboon.logging import logger
from gaboon.utils._cli_constants import DEFAULT_KEYSTORES_PATH
from eth_account import Account as EthAccountsClass
from eth_account.signers.local import LocalAccount


def main(args: List[Any]) -> int:
    if args.wallet_command == "list":
        list_accounts()
        return 0
    elif args.wallet_command == "generate":
        return generate_account(
            args.name,
            args.save,
            password=args.password,
            password_file=args.password_file,
        )
    elif args.wallet_command == "address":
        return convert_to_address(args.private_key)
    elif args.wallet_command == "sign":
        return sign_message(args.message, args.private_key)
    elif args.wallet_command == "verify":
        return verify_signature(args.message, args.signature, args.address)
    elif args.wallet_command == "import":
        return import_private_key(args.private_key)
    elif args.wallet_command == "export":
        return export_account(args.address)
    elif args.wallet_command == "password":
        return change_password(args.address)
    elif args.wallet_command == "private-key":
        return derive_private_key(args.mnemonic)
    elif args.wallet_command == "decrypt-keystore":
        return decrypt_keystore(args.keystore_file)
    else:
        logger.error(f"Unknown accounts command: {args.wallet_command}")
        return 1


def list_accounts(
    keystores_path: Path = DEFAULT_KEYSTORES_PATH,
) -> list[Any] | None:
    if keystores_path.exists():
        account_paths = sorted(keystores_path.glob("*"))
        logger.info(
            f"Found {len(account_paths)} account{'s' if len(account_paths)!=1 else ''}:"
        )
        for path in account_paths:
            logger.info(f"{path.stem}")
        return account_paths
    else:
        logger.info(f"No accounts found at {keystores_path}")
        return None


def generate_account(
    name: str, save: bool = False, password: str = None, password_file: str = None
) -> int:
    logger.info("Generating new account...")
    new_account: LocalAccount = EthAccountsClass.create()
    if save:
        if password:
            save_to_keystores(
                name,
                new_account,
                password=password,
                keystores_path=DEFAULT_KEYSTORES_PATH,
            )
        elif password_file:
            save_to_keystores(
                name,
                new_account,
                password_file=Path(password_file),
                keystores_path=DEFAULT_KEYSTORES_PATH,
            )
        else:
            logger.error("No password provided to save account")
            return 1
    else:
        logger.info(f"Account generated: {new_account.address}")
        logger.info(f"(Unsafe) Private key: {new_account.key}")
        logger.info(
            f"To save, add the --save flag next time with:\ngab wallet generate {name} --save --password <password>"
        )
    return 0


def save_to_keystores(
    name: str,
    account: LocalAccount,
    password: str = None,
    password_file: Path | None = None,
    keystores_path: Path = DEFAULT_KEYSTORES_PATH,
):
    new_keystore_path = keystores_path.joinpath(name)
    if new_keystore_path.exists():
        logger.error(f"Account with name {name} already exists")
        return 1
    new_keystore_path.mkdir(exist_ok=True)
    json_file = new_keystore_path.joinpath(name).resolve()
    if password:
        encrypted: dict[str, Any] = account.encrypt(password)
    elif password_file:
        with password_file.open("r") as fp:
            password = fp.read()
        encrypted: dict[str, Any] = account.encrypt(password)
    else:
        logger.error("No password provided to save account")
        return 1
    with json_file.open("w") as fp:
        json.dump(encrypted, fp)
    logger.info(f"Saved account {name} to keystores!")


def convert_to_address(project: Project, private_key: str) -> int:
    logger.info(f"Converting private key to address...")
    # Implement conversion logic here
    return 0


def sign_message(project: Project, message: str, private_key: str) -> int:
    logger.info(f"Signing message...")
    # Implement message signing logic here
    return 0


def verify_signature(
    project: Project, message: str, signature: str, address: str
) -> int:
    logger.info(f"Verifying signature...")
    # Implement signature verification logic here
    return 0


def import_private_key(project: Project, private_key: str) -> int:
    logger.info(f"Importing private key...")
    # Implement private key import logic here
    return 0


def export_account(project: Project, address: str) -> int:
    logger.info(f"Exporting account...")
    # Implement account export logic here
    return 0


def change_password(project: Project, address: str) -> int:
    logger.info(f"Changing account password...")
    # Implement password change logic here
    return 0


def derive_private_key(project: Project, mnemonic: str) -> int:
    logger.info(f"Deriving private key from mnemonic...")
    # Implement private key derivation logic here
    return 0


def decrypt_keystore(project: Project, keystore_file: str) -> int:
    logger.info(f"Decrypting keystore...")
    # Implement keystore decryption logic here
    return 0
