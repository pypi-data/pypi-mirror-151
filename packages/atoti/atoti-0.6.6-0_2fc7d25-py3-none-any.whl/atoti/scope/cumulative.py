from typing import Optional, Union

from atoti_core import is_date_type

from ..level import Level
from ._utils import CumulativeWindow, TimePeriodWindow
from .scope import Scope


def cumulative(
    level: Level,
    *,
    dense: bool = False,
    partitioning: Optional[Level] = None,
    window: Union[Optional[range], TimePeriodWindow] = None,
) -> Scope:
    """Create a scope to be used in the computation of cumulative aggregations.

    Cumulative aggregations include cumulative sums (also called running sum or prefix sum), mean, min, max, etc.

    Args:
        level: The level along which the aggregation is performed.
        dense: When ``True``, all members of the level, even those with no value for the underlying measure, will be taken into account for the cumulative aggregation (resulting in repeating values).
        partitioning: The levels in the hierarchy at which to start the aggregation over.
        window: The custom aggregation window.
            The window defines the set of members before and after a given member (using the level order) to be considered in the computation of the cumulative aggregation.

            The window can be a:

            * ``range`` starting with a <=0 value and ending with a >=0 value.

               By default the window is ``range(-∞, 0)``, meaning that the value for a given member is computed using all of the members before it and none after it.

               For instance, to compute the sliding mean on the 5 previous members of a level::

                 m2 = atoti.agg.mean(m1, scope=tt.scope.cumulative(l["date"], window=range(-5, 0)))

            * time period as a two-element tuple starting with an offset of the form ``-xxDxxWxxMxxQxxY`` or ``None`` and ending with an offset of the form ``xxDxxWxxMxxQxxY`` or ``None``.

              Example:

                >>> from datetime import date
                >>> df = pd.DataFrame(
                ...     columns=["Date", "Quantity"],
                ...     data=[
                ...         (date(2019, 7, 2), 15),
                ...         (date(2019, 7, 1), 20),
                ...         (date(2019, 6, 1), 25),
                ...         (date(2019, 6, 2), 15),
                ...         (date(2019, 6, 30), 5),
                ...     ],
                ... )
                >>> table = session.read_pandas(df, table_name="CumulativeTimePeriod")
                >>> cube = session.create_cube(table, mode="manual")
                >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
                >>> cube.create_date_hierarchy("Date", column=table["Date"])
                >>> h["Date"] = {
                ...     **h["Date"].levels,
                ...     "Date": table["Date"],
                ... }
                >>> m["Quantity.SUM"] = tt.agg.sum(table["Quantity"])
                >>> m["Cumulative quantity"] = tt.agg.sum(
                ...     m["Quantity.SUM"], scope=tt.scope.cumulative(l["Date"])
                ... )
                >>> m["Cumulative quantity with 2 days window"] = tt.agg.sum(
                ...     m["Quantity.SUM"],
                ...     scope=tt.scope.cumulative(l["Date"], window=("-2D", None)),
                ... )
                >>> m[
                ...     "Cumulative quantity with 2 days window partitioned by month"
                ... ] = tt.agg.sum(
                ...     m["Quantity.SUM"],
                ...     scope=tt.scope.cumulative(
                ...         l["Date"], window=("-2D", None), partitioning=l["Month"]
                ...     ),
                ... )
                >>> cube.query(
                ...     m["Quantity.SUM"],
                ...     m["Cumulative quantity"],
                ...     m["Cumulative quantity with 2 days window"],
                ...     m[
                ...         "Cumulative quantity with 2 days window partitioned by month"
                ...     ],
                ...     levels=[l["Day"]],
                ...     include_totals=True,
                ... )
                                Quantity.SUM Cumulative quantity Cumulative quantity with 2 days window Cumulative quantity with 2 days window partitioned by month
                Year  Month Day
                Total                     80                  80                                     40
                2019                      80                  80                                     40
                      6                   45                  45                                      5                                                  5
                            1             25                  25                                     25                                                 25
                            2             15                  40                                     40                                                 40
                            30             5                  45                                      5                                                  5
                      7                   35                  80                                     40                                                 35
                            1             20                  65                                     25                                                 20
                            2             15                  80                                     40                                                 35

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Year", "Month", "Day", "Quantity"],
        ...     data=[
        ...         (2019, 7, 1, 15),
        ...         (2019, 7, 2, 20),
        ...         (2019, 6, 1, 25),
        ...         (2019, 6, 2, 15),
        ...         (2018, 7, 1, 5),
        ...         (2018, 7, 2, 10),
        ...         (2018, 6, 1, 15),
        ...         (2018, 6, 2, 5),
        ...     ],
        ... )
        >>> table = session.read_pandas(df, table_name="Cumulative")
        >>> cube = session.create_cube(table)
        >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
        >>> h["Date"] = [table["Year"], table["Month"], table["Day"]]
        >>> m["Quantity.SUM"] = tt.agg.sum(table["Quantity"])
        >>> m["Cumulative quantity"] = tt.agg.sum(
        ...     m["Quantity.SUM"], scope=tt.scope.cumulative(l["Day"])
        ... )
        >>> m["Cumulative quantity partitioned by month"] = tt.agg.sum(
        ...     m["Quantity.SUM"],
        ...     scope=tt.scope.cumulative(l["Day"], partitioning=l["Month"]),
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     m["Cumulative quantity"],
        ...     m["Cumulative quantity partitioned by month"],
        ...     levels=[l["Day"]],
        ...     include_totals=True,
        ... )
                        Quantity.SUM Cumulative quantity Cumulative quantity partitioned by month
        Year  Month Day
        Total                    110                 110
        2018                      35                  35
              6                   20                  20                                       20
                    1             15                  15                                       15
                    2              5                  20                                       20
              7                   15                  35                                       15
                    1              5                  25                                        5
                    2             10                  35                                       15
        2019                      75                 110
              6                   40                  75                                       40
                    1             25                  60                                       25
                    2             15                  75                                       40
              7                   35                 110                                       35
                    1             15                  90                                       15
                    2             20                 110                                       35

    """
    if isinstance(window, tuple):
        if not is_date_type(level.data_type.java_type):
            raise ValueError(
                "Time period window can only be used with hierarchy whose deepest level is temporal."
            )
        if isinstance(window, range) and window.step != 1:
            raise ValueError(
                "Running aggregation windows only support ranges with step of size 1."
            )
    return CumulativeWindow(
        _level_coordinates=level._coordinates,
        _dense=dense,
        _window=window,
        _partitioning=partitioning._coordinates if partitioning is not None else None,
    )
