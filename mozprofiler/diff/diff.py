import os
import pstats

from tabulate import tabulate


class Diff:
    def __init__(self, previous_profile, latest_profile):
        self.previous = pstats.Stats(previous_profile)
        self.latest = pstats.Stats(latest_profile)
        self.repos = r"(review|lando-api|lando-ui)"
        self.previous_cmd = os.path.basename(previous_profile).split("_")[0]
        self.latest_cmd = os.path.basename(latest_profile).split("_")[0]

    def sort_profiles(self, sort_by):
        keys = {
            "ctime": pstats.SortKey.CUMULATIVE,
            "calls": pstats.SortKey.CALLS,
        }

        self.previous.sort_stats(keys[sort_by])
        self.latest.sort_stats(keys[sort_by])

    def print_stats(self):
        prev_time, latest_time = self._get_time()
        table = [
            [f"Total Time: {prev_time}s", f"Total Time: {latest_time}s"],
        ]
        print(
            tabulate(table, headers=(
                f"{' '.join(self.previous_cmd.split('.'))} (previous)",
                f"{' '.join(self.latest_cmd.split('.'))} (latest)",
            ))
        )

    def _get_time(self):
        prev_time = self.previous.get_stats_profile().total_tt
        latest_time = self.latest.get_stats_profile().total_tt

        return prev_time, latest_time



