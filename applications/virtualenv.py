import os
import sys
import venv


class VirtualEnvironment:
    def __init__(self, path: str, name: str, force_create: bool = False):
        self._name = f"moz-profiler-venv-{name}"
        self._path = f"{path}/{self.name}"

        if os.path.exists(self.path) and not force_create:
            return

        print("Creating virtual environment...")

        venv.create(
            env_dir=self.path,
            clear=force_create,
            with_pip=True,
            prompt=".",
        )

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def activate(self):
        if f"{self.path}/bin" not in sys.path:
            sys.path.insert(0, f"{self.path}/bin")

