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
"""CLI command implementations."""
import argparse
import ast
import pathlib
import subprocess

from alembic_versions.config import Settings
from rich.console import Console
from rich.table import Table


def _run_git_command(git: pathlib.Path, command: list[str]) -> str:
    """Run a git command and return stdout."""
    completed = subprocess.run(
        [str(git), *command],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _migration_message(migration_path: pathlib.Path) -> str:
    """Parse the migration's human-readable message from its module docstring."""
    fallback = migration_path.stem.split("_", maxsplit=1)
    fallback_message = (
        fallback[1].replace("_", " ").strip()
        if len(fallback) > 1
        else migration_path.stem
    )

    try:
        with migration_path.open("r", encoding="utf-8") as stream:
            module = ast.parse(stream.read())
    except (OSError, SyntaxError):
        return fallback_message

    docstring = ast.get_docstring(module)
    if not docstring:
        return fallback_message

    first_line = next((line.strip() for line in docstring.splitlines() if line.strip()), "")
    return first_line or fallback_message


def branch(settings: Settings, args: argparse.Namespace):
    """Find new alembic migrations added in the current branch."""
    del settings  # not used by this command
    console = Console()
    versions_path = pathlib.Path(args.versions)
    versions_glob = f"{versions_path.as_posix().rstrip('/') or '.'}/*.py"

    try:
        base = _run_git_command(
            args.git,
            ["merge-base", "HEAD", args.base],
        )
        migration_files = _run_git_command(
            args.git,
            ["diff", "--name-only", "--diff-filter=A", f"{base}..HEAD", "--", versions_glob],
        ).splitlines()
    except subprocess.CalledProcessError as err:
        console.print(f"[red]Git command failed:[/red] {err.stderr.strip() or err}")
        return 1

    if not migration_files:
        console.print("[yellow]No new alembic migrations found in this branch.[/yellow]")
        return 0

    table = Table(title="New Alembic Migrations", show_header=True, header_style="bold cyan")
    table.add_column("Revision", style="green", no_wrap=True)
    table.add_column("Message", style="magenta")

    for migration_file in migration_files:
        migration_path = pathlib.Path(migration_file)
        revision = migration_path.stem.split("_", maxsplit=1)[0]
        message = _migration_message(migration_path)
        table.add_row(revision, message)

    console.print(table)
    return 0
