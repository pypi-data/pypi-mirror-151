import multiprocessing
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator, Optional, Sequence

import attr
import psycopg
from psycopg import Transaction
from psycopg.rows import RowFactory, dict_row
from psycopg_pool import ConnectionPool

from .typing import Parameters, Query, Row

__all__ = [
    "Database",
    "TransactionManager",
    "connect",
]

_txn: ContextVar[Optional[Transaction]] = ContextVar("_txn")

DEFAULT_MIN_POOL_SIZE = (multiprocessing.cpu_count() * 2) + 1
DEFAULT_MAX_POOL_SIZE = DEFAULT_MIN_POOL_SIZE * 2


@attr.frozen(kw_only=True)
class Database:
    _pool: ConnectionPool

    @classmethod
    def connect(
        cls,
        conninfo: str,
        min_size: int = DEFAULT_MIN_POOL_SIZE,
        max_size: int = DEFAULT_MAX_POOL_SIZE,
    ) -> "Database":
        return cls(
            pool=ConnectionPool(
                conninfo=conninfo,
                min_size=min_size,
                max_size=max_size,
            ),
        )

    def close(self, timeout: float = 0.5):
        return self._pool.close(timeout=timeout)

    @contextmanager
    def connection(self) -> Iterator[psycopg.Connection[Any]]:
        try:
            yield _txn.get().connection
        except LookupError:
            with self._pool.connection() as conn:
                conn.autocommit = True
                yield conn

    @contextmanager
    def cursor(self, row_factory: Optional[RowFactory] = None) -> Iterator[psycopg.Cursor[Any]]:
        with self.connection() as conn:
            with conn.cursor(row_factory=row_factory) as cur:
                yield cur

    def execute(
        self,
        query: Query,
        params: Optional[Parameters] = None,
    ):
        with self.cursor() as cur:
            cur.execute(query, params)

    def query_one(
        self,
        query: Query,
        params: Optional[Parameters] = None,
    ) -> Optional[Row]:
        with self.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def query(
        self,
        query: Query,
        params: Optional[Parameters] = None,
    ) -> Sequence[Row]:
        with self.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            return cur.fetchall()


@attr.frozen(kw_only=True)
class TransactionManager:
    _db: Database

    @contextmanager
    def transaction(
        self,
        savepoint_name: Optional[str] = None,
        force_rollback: bool = False,
    ) -> Iterator[Transaction]:
        with self._db.connection() as conn:
            with conn.transaction(savepoint_name, force_rollback) as tx:
                try:
                    token = _txn.set(tx)
                    yield tx
                finally:
                    _txn.reset(token)


def connect(
    conninfo: str,
    min_size: int = DEFAULT_MIN_POOL_SIZE,
    max_size: int = DEFAULT_MAX_POOL_SIZE,
) -> Database:
    return Database.connect(
        conninfo,
        min_size=min_size,
        max_size=max_size,
    )
