import argparse

from mozprofiler.utils.helpers import generate_application


def detach(args: argparse.Namespace):
    app = generate_application(args.application, False)
    app.detach()


def add_parser(parser):
    detach_parser = parser.add_parser(
        "detach", help="Deactivate profiling for a specific application."
    )
    detach_parser.add_argument(
        "application", type=str, help="Which application to deactivate."
    )
    detach_parser.set_defaults(func=detach)
