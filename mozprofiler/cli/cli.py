import argparse
import sys
import textwrap

from . import commands

from importlib import import_module
from typing import List, Set

from mozprofiler.utils.storage import storage


class CommandLineInterface:
    def __init__(self):
        self.path = storage.get("moz-profiler-path")
        self.args = None
        if not self.path:
            self.path = "/".join(
                commands.__file__.split("/")[:-3],
            )
            storage.store({"moz-profiler-path": self.path})

    def __parse_args(self, argv: List[str]):
        self.main_parser = argparse.ArgumentParser(
            prog="moz-profiler",
            description="A tool for profiling Mozilla Conduit applications.",
            add_help=False,
        )
        self.main_parser.add_argument("--version", action="store_true", help=argparse.SUPPRESS)
        self.main_parser.add_argument(
            "--trace", "--debug", action="store_true", help=argparse.SUPPRESS
        )

        self.parser = argparse.ArgumentParser(
            parents=[self.main_parser],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """
                If moz-profiler is executed without specifying a command, the 'attach' command
                will be executed.
                For more help on 'attach' and its options run 'moz-profiler attach --help'.
                """
            ),
        )

        commands_parser = self.parser.add_subparsers(
            dest="command",
            metavar="COMMAND",
            description="For full command description: moz-profiler COMMAND -h",
        )
        commands_parser.required = True

        for command in commands.__all__:
            module = import_module("mozprofiler.cli.commands.{}".format(command))
            add_parser = getattr(module, "add_parser", None)
            if callable(add_parser):
                add_parser(commands_parser)

        self.help_parser = commands_parser.add_parser("help")
        self.help_parser.add_argument("command", nargs=argparse.OPTIONAL)
        self.help_parser.set_defaults(print_help=True)

        fallback = self.__should_fallback_to_attach(
            argv, {command for command in commands_parser.choices}
        )
        if fallback:
            argv.insert(0, "attach")

        main_args, unknown = self.main_parser.parse_known_args(argv)

        # map --version to the 'version' command
        if main_args.version:
            unknown = ["version"]

        args = self.parser.parse_args(unknown)

        # copy across parsed main_args; they are defined in `args`, but not set
        for name, value in vars(main_args).items():
            args.__setattr__(name, value)

        args.fallback = fallback

        # handle the help command here as printing help needs access to the parser
        if hasattr(args, "print_help"):
            help_argv = ["--help"]
            if args.command:
                help_argv.insert(0, args.command)
            # parse_args calls parser.exit() when passed --help
            self.parser.parse_args(help_argv)

        self.args = args

    @staticmethod
    def __should_fallback_to_attach(argv: List[str], cmds: Set[str]) -> bool:
        """Return `True` if `moz-profiler` should fallback to `attach` command."""
        # Just running `moz-profiler` with no arguments means fallback.
        if not argv:
            return True

        # Don't fallback if help args are passed.
        if any(help_arg in set(argv) for help_arg in {"-h", "--help"}):
            return False

        # Don't fallback if a known command is passed.
        if argv[0] in cmds:
            return False

        return True

    def exec(self, argv: List[str]):
        self.__parse_args(argv)
        self.args.func(self.args)


def run():
    cli = CommandLineInterface()
    cli.exec(argv=sys.argv[1:])


if __name__ == "__main__":
    run()
