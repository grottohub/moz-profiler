import argparse

from utils.storage import Storage


def storage(args: argparse.Namespace):
    store = Storage()
    print(store.get(args.key))


def add_parser(parser):
    storage_parser = parser.add_parser(
        "storage", help="Access storage items by key."
    )
    storage_parser.add_argument(
        "key", type=str, help="The key to access."
    )
    storage_parser.set_defaults(func=storage)