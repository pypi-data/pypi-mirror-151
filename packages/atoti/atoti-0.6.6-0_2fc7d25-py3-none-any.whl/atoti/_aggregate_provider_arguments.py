from dataclasses import dataclass, field
from typing import Iterable, Literal

from atoti_core import LevelCoordinates, keyword_only_dataclass


@keyword_only_dataclass
@dataclass(frozen=True)
class AggregateProviderArguments:
    name: str = field(compare=False)
    key: Literal["bitmap", "leaf"]
    levels_coordinates: Iterable[LevelCoordinates] = ()
    measures_names: Iterable[str] = ()
