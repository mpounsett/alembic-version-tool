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
"""Logging helpers."""
import logging

from rich.logging import RichHandler


def setup_logging(level: int | str = logging.INFO) -> None:
    """Configure colorized console logging with Rich."""
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=level,
        datefmt="[%X]",
        handlers=[
            RichHandler(
                markup=True,
                rich_tracebacks=True,
                show_path=False,
            )
        ],
        force=True,
    )
