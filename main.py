import cProfile
import os
import pathlib
import shutil
import subprocess
import sys

from datetime import datetime


def cleanup(cwd):
    print("Cleaning up...")
    os.chdir(cwd)
    shutil.rmtree(cwd.joinpath("review"))


def init(cwd):
    print("Beginning profiler for moz-phab...")
    print("Cloning review into ~/profiling...")
    subprocess.run(
        ["git", "clone", "https://github.com/mozilla-conduit/review.git"],
        cwd=cwd,
    )
    os.chdir(cwd.joinpath("review"))
    subprocess.run(
        ["python", "-m", "venv", "venv"],
    )
    subprocess.run(
        ["venv/bin/pip", "install", "-r", "dev/requirements/python3.9.txt"]
    )
    subprocess.run(
        ["venv/bin/pip", "install", "-e", "."]
    )


def profile_mozphab(patch, prof, src="venv/bin/moz-phab"):
    with cProfile.Profile() as profile:
        subprocess.run(
            [src, "patch", patch, "--apply-to", "here", "--trace"]
        )
    profile.dump_stats(prof)


if __name__ == "__main__":
    cwd = pathlib.Path(os.getcwd())
    init(cwd)
    prof = datetime.now().strftime("profiles/%d-%m-%Y_%H:%M:%S.prof")
    profile_mozphab(sys.argv[1], cwd.joinpath(prof))

    subprocess.run([
        "git", "switch", "main"
    ])

    diff_src = "/Users/grobertson/review/venv/bin/moz-phab"
    prof_two = datetime.now().strftime("profiles/%d-%m-%Y_%H:%M:%S.prof")
    profile_mozphab(sys.argv[1], cwd.joinpath(prof_two), src=diff_src)
    cleanup(cwd)
    print("To launch snakeviz run:")
    print(f"\tsnakeviz {prof}")
    print(f"\tsnakeviz {prof_two}")
