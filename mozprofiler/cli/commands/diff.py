import argparse

from mozprofiler.diff.diff import Diff
from mozprofiler.utils.storage import storage


def diff(args: argparse.Namespace):
    previous_profile = storage.get("previous-profile")
    latest_profile = storage.get("latest-profile")
    if not previous_profile or not latest_profile:
        raise Exception("Not enough profiles to compare.")

    d = Diff(previous_profile, latest_profile)
    d.sort_profiles(args.sort_by)
    d.print_stats()


def add_parser(parser):
    diff_parser = parser.add_parser(
        "diff", help="Compare the profiles of the last two executions."
    )
    diff_parser.add_argument(
        "--sort-by",
        type=str,
        choices=["ctime", "calls"],
        help="How to sort the results.",
        required=True,
    )
    diff_parser.set_defaults(func=diff)
