import argparse

from utils.helpers import generate_application


def run(args: argparse.Namespace):
    app = generate_application(
        application=args.application,
        force_recreate=False,
    )
    app.run(args=args.args)


def add_parser(parser):
    run_parser = parser.add_parser(
        "run", help="Execute an attached application."
    )
    run_parser.add_argument(
        "application", type=str, help="The application to execute."
    )
    run_parser.add_argument(
        "--args", type=str, help="Arguments to pass to the application."
    )
    run_parser.add_argument(
        "--ignore-help", action="store_true", help="Ignore the --help flag, for internal use."
    )
    run_parser.set_defaults(func=run)
