import cProfile
import os
import subprocess
import sys
from datetime import datetime
from importlib import import_module
from types import ModuleType

from mozprofiler.applications.application import Application
from mozprofiler.applications.virtualenv import VirtualEnvironment
from mozprofiler.utils.storage import storage
from mozprofiler.utils.utils import load_rc_file_in_place, get_rc_file


class MozPhabApplication(Application):
    def __init__(self, application_name, path=None, force_recreate=False):
        super().__init__(application_name, path, force_recreate)

        self.requirements = "/".join([
            self.path,
            "dev",
            "requirements",
            "python3.9.txt",
        ])

        self.venv = VirtualEnvironment(
            path=self.path,
            name=self.name,
            force_create=force_recreate
        )

        moz_profiler_path = storage.get("moz-profiler-path")
        self.exports = [
            f"export MOZ_PROFILER_PATH={moz_profiler_path}",
            f"export MOZPHAB_PROFILER_VENV={self.venv.path}",
            f"export PATH=$MOZ_PROFILER_PATH/bin:$PATH",
        ]

        self.mozphab = None
        storage.store({"moz-phab-path": self.path})

    def run(self, args: str):
        self.venv.activate()

        # Resubstitute argument signifiers.
        args = args.replace("+", "-")
        argv = ["moz-phab", *args.split(" ")]

        # Replace moz-profiler args with intercepted moz-phab args
        sys.argv = argv

        try:
            self.mozphab = self._import()
        except ModuleNotFoundError:
            self._install()
            self.mozphab = self._import()

        profile_dir = storage.get("profile-path")
        date = datetime.now().strftime("%m-%d-%Y")
        profile_name = ".".join(argv)
        profile_time = datetime.now().strftime("%H:%M:%S")

        try:
            os.mkdir(f"{profile_dir}/{date}")
        except FileExistsError:
            pass

        profile = f"{profile_dir}/{date}/{profile_name}_{profile_time}.prof"

        cProfile.runctx(
            "self.mozphab.run()",
            globals(),
            locals(),
            filename=profile,
        )

        previous = storage.get("latest-profile")
        storage.store({
            "previous-profile": previous,
            "latest-profile": profile,
        })

    def _import(self, path: str = None) -> ModuleType:
        path = path or self.path
        sys.path.insert(0, path)
        mozphab = import_module("mozphab.mozphab")
        return mozphab

    def attach(self):
        self._link()
        self._install()
        print(f"Run `source {get_rc_file()}` to finish attaching the profiler.")

    def detach(self):
        self._unlink()
        print(f"Run `source {get_rc_file()}` to finish detaching the profiler.")

    def _link(self):
        is_linked = storage.get("moz-phab-is-linked")
        if not is_linked:
            with open(get_rc_file(), "a") as rc_a:
                rc_a.write(
                    f"\n# This section added by moz-profiler\n"
                    f"{self.exports[0]}\n"
                    f"{self.exports[1]}\n"
                    f"{self.exports[2]}\n"
                )
            storage.store({"moz-phab-is-linked": True})
        else:
            with load_rc_file_in_place() as rc:
                for line in rc:
                    if line.strip() == f"# {self.exports[0]}":
                        print(f"{self.exports[0]}\n", end="")
                    elif line.strip() == f"# {self.exports[1]}":
                        print(f"{self.exports[1]}\n", end="")
                    elif line.strip() == f"# {self.exports[2]}":
                        print(f"{self.exports[2]}\n", end="")
                    else:
                        print(line, end="")

    def _unlink(self):
        with load_rc_file_in_place() as rc:
            for line in rc:
                try:
                    idx = self.exports.index(line.strip())
                    print(line.replace(
                        self.exports[idx],
                        f"# {self.exports[idx]}"
                    ), end="")
                except ValueError:
                    print(line, end="")
                    pass

    def _install(self):
        self.venv.activate()
        print("Installing dependencies...")
        subprocess.run(
            [
                "pip3",
                "install",
                "-r",
                self.requirements,
            ],
            cwd=self.path,
        )
        subprocess.run(["pip3", "install", "-e", self.path], cwd=self.path)
