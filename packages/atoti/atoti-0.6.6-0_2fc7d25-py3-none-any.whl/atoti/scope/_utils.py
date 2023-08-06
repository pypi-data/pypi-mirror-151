from abc import abstractmethod
from dataclasses import dataclass
from typing import Collection, Optional, Tuple, Union

from atoti_core import (
    HierarchyCoordinates,
    LevelCoordinates,
    coordinates_to_java_description,
    keyword_only_dataclass,
)

from .._measures.generic_measure import GenericMeasure
from ..measure_description import MeasureDescription
from .scope import Scope

TimePeriodWindow = Union[
    Tuple[str, str], Tuple[Optional[str], str], Tuple[str, Optional[str]]
]


@keyword_only_dataclass
# See https://github.com/python/mypy/issues/5374.
@dataclass(frozen=True)  # type: ignore[misc]
class Window(Scope):
    """Window-like structure used in the computation of cumulative aggregations."""

    @abstractmethod
    def _create_aggregated_measure(
        self, measure: MeasureDescription, agg_fun: str
    ) -> MeasureDescription:
        """Create the appropriate aggregated measure for this window.

        Args:
            measure: The underlying measure to aggregate
            agg_fun: The aggregation function to use.
        """


@keyword_only_dataclass
@dataclass(frozen=True)
class CumulativeWindow(Window):
    """Implementation of a Window for member-based cumulative aggregations."""

    _level_coordinates: LevelCoordinates
    _dense: bool
    _window: Union[TimePeriodWindow, Optional[range]] = None
    _partitioning: Optional[LevelCoordinates] = None

    def _create_aggregated_measure(
        self, measure: MeasureDescription, agg_fun: str
    ) -> MeasureDescription:
        return GenericMeasure(
            "WINDOW_AGG",
            measure,
            coordinates_to_java_description(self._level_coordinates),
            coordinates_to_java_description(self._partitioning)
            if self._partitioning is not None
            else None,
            agg_fun,
            (self._window.start, self._window.stop)
            if isinstance(self._window, range)
            else self._window,
            self._dense,
        )


@keyword_only_dataclass
@dataclass(frozen=True)
class SiblingsWindow(Window):
    """Implementation of a Window for sibling aggregations.

    It contains at least hierarchy, and whether to exclude the current member from the calculations (useful when computing marginal aggregations).
    """

    _hierarchy_coordinates: HierarchyCoordinates
    _exclude_self: bool = False

    def _create_aggregated_measure(
        self, measure: MeasureDescription, agg_fun: str
    ) -> MeasureDescription:
        return GenericMeasure(
            "SIBLINGS_AGG",
            measure,
            coordinates_to_java_description(self._hierarchy_coordinates),
            agg_fun,
            self._exclude_self,
        )


@dataclass(frozen=True)
class LeafLevels(Scope):  # pylint: disable=keyword-only-dataclass
    """A collection of levels coordinates, used in dynamic aggregation operations."""

    _levels_coordinates: Collection[LevelCoordinates]

    @property
    def levels_coordinates(self) -> Collection[LevelCoordinates]:
        """Dynamic aggregation levels."""
        return self._levels_coordinates
