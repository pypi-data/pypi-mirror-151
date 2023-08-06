from dataclasses import dataclass
from typing import Any, Collection, Literal

from atoti_core import keyword_only_dataclass

from ._aggregate_provider_arguments import AggregateProviderArguments
from .level import Level
from .measure import Measure

AggregateProviderKey = Literal["bitmap", "leaf"]


@keyword_only_dataclass
@dataclass(frozen=True)
class AggregateProvider:
    """Aggregate providers are optimizations to pre-aggregate some table columns up to certain levels.

    If a step of a query uses a subset of the aggregate provider's levels and measures it can use this provider and thus speed up the query.

    Aggregate providers use additional memory since they store the intermediate aggregates.

    The more levels and measures are added, the more memory is required.

    Args:
        key: The key of the provider.
          ``"bitmap"`` is generally faster but also takes more memory.
        levels: The levels to build the provider on.
        measures: The measures to put in the provider."""

    key: AggregateProviderKey = "leaf"
    levels: Collection[Level] = ()
    measures: Collection[Measure] = ()

    def _to_arguments(self, *, name: str) -> AggregateProviderArguments:
        return AggregateProviderArguments(
            name=name,
            key=self.key,
            levels_coordinates=[level._coordinates for level in self.levels],
            measures_names=[measure.name for measure in self.measures],
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AggregateProvider):
            return False
        return self._to_arguments(name="") == other._to_arguments(name="")
