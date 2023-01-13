import argparse

from mozprofiler.utils.helpers import generate_application


def attach(args: argparse.Namespace):
    app = generate_application(
        application=args.application,
        force_recreate=args.force_recreate,
    )
    app.attach()


def add_parser(parser):
    attach_parser = parser.add_parser(
        "attach", help="Activate profiling for a specific application."
    )
    attach_parser.add_argument(
        "application", type=str, help="Which application to profile."
    )
    attach_parser.add_argument(
        "--force-recreate", action="store_true", help="Whether or not to recreate a virtual environment."
    )
    attach_parser.set_defaults(func=attach)
