from __future__ import annotations

import platform
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional
from uuid import UUID, uuid4

from atoti_core import get_env_flag, keyword_only_dataclass

from .._path_utils import get_atoti_home
from .._version import VERSION
from .event import Event

_INSTALLATION_ID_PATH = get_atoti_home() / "installation_id.txt"


def _get_installation_id_from_file() -> Optional[str]:
    if not _INSTALLATION_ID_PATH.exists():
        return None

    try:
        content = _INSTALLATION_ID_PATH.read_text(encoding="utf8").strip()
        UUID(content)
        return content
    except (OSError, ValueError):
        # The file cannot be read or its content is not a valid UUID.
        return None


def _write_installation_id_to_file(installation_id: str) -> None:
    try:
        _INSTALLATION_ID_PATH.parent.mkdir(
            exist_ok=True,
            parents=True,
        )
        _INSTALLATION_ID_PATH.write_text(f"{installation_id}\n", encoding="utf8")
    except OSError:
        # To prevent bothering the user, do nothing even if the id could not be written to the file.
        ...


@lru_cache
def _get_installation_id() -> str:
    existing_id = _get_installation_id_from_file()

    if existing_id is not None:
        return existing_id

    new_id = str(uuid4())

    _write_installation_id_to_file(new_id)

    return new_id


def _get_environment() -> Optional[str]:
    return "CI" if get_env_flag("CI") else None


@keyword_only_dataclass
@dataclass(frozen=True)
class ImportEvent(Event):
    """Triggered when the library is imported."""

    event_type: str = field(default="import", init=False)
    installation_id: str = field(default_factory=_get_installation_id, init=False)
    operating_system: str = field(default_factory=platform.platform, init=False)
    python_version: str = field(default_factory=platform.python_version, init=False)
    version: str = field(default=VERSION, init=False)
    environment: Optional[str] = field(default_factory=_get_environment, init=False)
