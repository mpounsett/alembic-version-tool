# ==============================================================================
#  Copyright 2026 Matthew Pounsett <matt@conundrum.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ==============================================================================
"""Main entry point for the Alembic Versions helper script."""
import argparse
import inspect
import logging
import pathlib
import sys
from typing import Optional

from alembic_versions.version import __version__
from alembic_versions import commands
from alembic_versions.config import Settings, load_settings
from alembic_versions.log import setup_logging

_LOG = logging.getLogger(__name__)

# Glory be to Jeppe Ledet-Pedersen!
# https://stackoverflow.com/a/13429281/951589
class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Format help for subcommands.

    Removes the redundant <command> from help output in subparsers.
    """

    def _format_action(self, action: argparse.Action) -> str:
        parts = super(SubcommandHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def parse_args(settings: Settings, args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    args = args or sys.argv[1:]

    parser = argparse.ArgumentParser(
        description=inspect.cleandoc("Help with managing alembic migrations in various ways."),
        formatter_class=SubcommandHelpFormatter,
    )
    parser.add_argument(
        '-v', '--version',
        action='version', version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(
        title='subcommands',
        description="%(prog)s has the following subcommands:",
    )

    ###################
    # START OF COMMANDS
    ###################

    branch_cmd = subparsers.add_parser(
        'branch',
        help="Find new alembic migrations added in the current branch",
    )
    branch_cmd.set_defaults(func=commands.branch)
    branch_cmd.add_argument(
        '-g', '--git',
        help="Path to git executable (default: %(default)s)",
        default=settings.git,
        type=pathlib.Path,
        metavar="PATH",
        required=False
    )
    branch_cmd.add_argument(
        '-v', '--versions',
        help="Path to alembic versions directory (default: %(default)s)",
        default=settings.versions,
        type=pathlib.Path,
        metavar="PATH",
        required=False
    )
    branch_cmd.add_argument(
        '-b', '--base',
        help="Base commit to compare against (default: %(default)s)",
        default=settings.commit_base,
        type=str,
        metavar="COMMIT",
    )

    #################
    # END OF COMMANDS
    #################

    args = parser.parse_args(args)

    # If any argument testing is to be done, do it here.

    return args


def main() -> None:
    """Main entry point."""
    setup_logging()
    settings = load_settings()
    if not settings:
        _LOG.error("Failed to load settings.")
        sys.exit(1)

    args = parse_args(settings)
    sys.exit(args.func(settings, args))

