from typing import Any, Dict, Mapping, Sequence, Union

from psycopg import sql

__all__ = [
    "Parameters",
    "Query",
    "Row",
]


Query = Union[str, sql.Composable]
Parameters = Union[Sequence[Any], Mapping[str, Any]]
Row = Dict[str, Any]
