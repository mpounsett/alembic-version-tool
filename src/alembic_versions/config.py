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
"""Configuration Settings."""
import logging
import pathlib

from typing import Optional

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

_LOG = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Main configuration settings.

    Attributes:
        git: Path to git executable.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="AV_",
        extra="ignore"
    )
    git: pathlib.Path = '/usr/bin/git'
    versions: pathlib.Path = './alembic/versions/'
    commit_base: str = 'origin/main'


def load_settings() -> Optional[Settings]:
    """Load the settings from environment variables.

    Returns:
        A Settings object.

    Raises:
        ValueError: If any of the settings values fail to validate.
    """
    try:
        settings = Settings()
    except ValidationError as err:
        _LOG.error(str(err))
        return None

    return settings
