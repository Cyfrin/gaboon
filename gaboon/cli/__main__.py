import importlib
import sys
from pathlib import Path
from gaboon.logging import logger, set_log_level
import tomllib
import argparse
from gaboon.project import Project

GAB_VERSION_STRING = "Gaboon v{}"


def main(argv: list) -> int:
    if "--version" in argv or "version" in argv:
        return get_version()

    main_parser = argparse.ArgumentParser(
        prog="Gaboon",
        description="🐍 Pythonic Smart Contract Development Framework",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    main_parser.add_argument(
        "-d", "--debug", action="store_true", help="Run in debug mode"
    )
    main_parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress all output except errors"
    )
    sub_parsers = main_parser.add_subparsers(dest="command")

    # Init command
    # ========================================================================
    init_parser = sub_parsers.add_parser(
        "init",
        help="Initialize a new project.",
        description="""
This will create a basic directory structure at the path you specific, which looks like:
.
├── README.md
├── gaboon.toml
├── script/
├── src/
│   └── Counter.vy
└── tests/
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    init_parser.add_argument(
        "path",
        help="Path of the new project, defaults to current directory.",
        type=Path,
        nargs="?",
        default=Path("."),
    )
    init_parser.add_argument(
        "-f",
        "--force",
        required=False,
        help="Overwrite existing project.",
        action="store_true",
    )

    # Compile command
    # ========================================================================
    sub_parsers.add_parser(
        "compile",
        help="Compiles the project.",
        description="""Compiles all Vyper contracts in the project. \n
This command will:
1. Find all .vy files in the src/ directory
2. Compile each file using the Vyper compiler
3. Output the compiled artifacts to the out/ directory

Use this command to prepare your contracts for deployment or testing.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        aliases=["build"],
    )

    # Run command
    # ========================================================================
    run_parser = sub_parsers.add_parser(
        "run",
        help="Runs a script with the project's context.",
        description="Runs a script with the project's context.",
    )
    run_parser.add_argument(
        "script_name_or_path",
        help="Name of the script in the script folder, or the path to your script.",
        type=str,
        default="./script/deploy.py",
    )
    run_parser.add_argument(
        "--rpc-url",
        help="RPC of the EVM network you'd like to deploy this code to.",
        type=str,
        nargs="?",
    )

    # Wallet command
    # ========================================================================
    wallet_parser = sub_parsers.add_parser(
        "wallet",
        help="Wallet management utilities.",
        description="Wallet management utilities.\n",
    )
    wallet_subparsers = wallet_parser.add_subparsers(dest="wallet_command")

    # List
    wallet_subparsers.add_parser(
        "list",
        aliases=["ls"],
        help="List all the accounts in the keystore default directory",
    )

    # Generate
    generate_parser = wallet_subparsers.add_parser(
        "generate",
        aliases=["g"],
        help="Create a new account with a random private key",
    )
    generate_parser.add_argument("name", help="Name of account")
    generate_parser.add_argument("--save", help="Save to keystore", action="store_true")
    # Create a group for password options
    password_group = generate_parser.add_mutually_exclusive_group()
    password_group.add_argument("--password", help="Password for the keystore")
    password_group.add_argument(
        "--password-file",
        help="File containing the password for the keystore",
    )
    # Add custom validation
    generate_parser.set_defaults(func=validate_generate_args)

    # Address
    address_parser = wallet_subparsers.add_parser(
        "address", aliases=["a", "addr"], help="Convert a private key to an address"
    )
    address_parser.add_argument("private_key", help="Private key to convert")

    # Sign
    sign_parser = wallet_subparsers.add_parser(
        "sign", aliases=["s"], help="Sign a message or typed data"
    )
    sign_parser.add_argument("message", help="Message or typed data to sign")
    sign_parser.add_argument("--private-key", help="Private key to sign with")

    # Verify
    verify_parser = wallet_subparsers.add_parser(
        "verify", aliases=["v"], help="Verify the signature of a message"
    )
    verify_parser.add_argument("message", help="Original message")
    verify_parser.add_argument("signature", help="Signature to verify")
    verify_parser.add_argument("address", help="Address of the signer")

    # Import
    import_parser = wallet_subparsers.add_parser(
        "import", aliases=["i"], help="Import a private key into an encrypted keystore"
    )
    import_parser.add_argument("private_key", help="Private key to import")

    # Export
    export_parser = wallet_subparsers.add_parser(
        "export", aliases=["e"], help="Export an existing account keystore file"
    )
    export_parser.add_argument("address", help="Address of the account to export")

    # Password
    password_parser = wallet_subparsers.add_parser(
        "password", help="Change the password of an existing account"
    )
    password_parser.add_argument(
        "address", help="Address of the account to change password"
    )

    # Private Key
    private_key_parser = wallet_subparsers.add_parser(
        "private-key", aliases=["pk"], help="Derives private key from mnemonic"
    )
    private_key_parser.add_argument("mnemonic", help="Mnemonic phrase")

    # Decrypt Keystore
    decrypt_keystore_parser = wallet_subparsers.add_parser(
        "decrypt-keystore",
        aliases=["dk"],
        help="Decrypt a keystore file to get the private key",
    )
    decrypt_keystore_parser.add_argument(
        "keystore_file", help="Path to the keystore file"
    )

    # Parsing starts
    if len(argv) == 0 or (len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help")):
        main_parser.print_help()
        return 0
    args = main_parser.parse_args(argv)

    set_log_level(quiet=args.quiet, debug=args.debug)

    if args.command != "wallet":
        try:
            project_root: Path = Project.find_project_root()
        except FileNotFoundError:
            if args.command != "init":
                logger.error(
                    "Not in a Gaboon project (or any of the parent directories).\nTry to create a gaboon.toml file with `gab init` "
                )
                return 1
            project_root = Path.cwd()
        if args.command == "build":
            args.command = "compile"
        args.project_root = project_root

    logger.info(f"Running {args.command} command...")
    if args.command:
        importlib.import_module(f"gaboon.cli.{args.command}").main(args)
    else:
        main_parser.print_help()
    return 0


def get_version() -> int:
    with open(
        Path(__file__).resolve().parent.parent.parent.joinpath("pyproject.toml"), "rb"
    ) as f:
        gaboon_data = tomllib.load(f)
        logger.info(GAB_VERSION_STRING.format(gaboon_data["project"]["version"]))
        return 0


def validate_generate_args(args):
    if args.save and not (args.password or args.password_file):
        raise argparse.ArgumentTypeError(
            "When using --save, you must provide either --password or --password-file"
        )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
