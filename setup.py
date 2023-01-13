from setuptools import setup

setup(
    name="moz-profiler",
    version="0.0.1",
    entry_points={
        "console_scripts": [
            "moz-profiler=cli.cli:run"
        ],
    },
)