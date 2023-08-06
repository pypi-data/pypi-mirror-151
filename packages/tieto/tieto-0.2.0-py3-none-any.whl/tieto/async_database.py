import multiprocessing
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any, Iterator, Optional, Sequence

import attr
import psycopg
from psycopg import AsyncConnection, AsyncCursor, AsyncTransaction
from psycopg.rows import RowFactory, dict_row
from psycopg_pool import AsyncConnectionPool

from .typing import Parameters, Query, Row

__all__ = [
    "AsyncDatabase",
    "AsyncTransactionManager",
]

_txn: ContextVar[Optional[AsyncTransaction]] = ContextVar("_txn")

DEFAULT_MIN_POOL_SIZE = (multiprocessing.cpu_count() * 2) + 1
DEFAULT_MAX_POOL_SIZE = DEFAULT_MIN_POOL_SIZE * 2


@attr.frozen(kw_only=True)
class AsyncDatabase:
    _pool: AsyncConnectionPool

    @classmethod
    def connect(
        cls,
        conninfo: str,
        min_size: int = DEFAULT_MIN_POOL_SIZE,
        max_size: int = DEFAULT_MAX_POOL_SIZE,
    ) -> "AsyncDatabase":
        return cls(
            pool=AsyncConnectionPool(
                conninfo=conninfo,
                min_size=min_size,
                max_size=max_size,
            ),
        )

    async def close(self, timeout: float = 0.5):
        return await self._pool.close(timeout=timeout)

    @asynccontextmanager
    async def connection(self) -> Iterator[AsyncConnection[Any]]:
        try:
            yield _txn.get().connection
        except LookupError:
            async with self._pool.connection() as conn:
                await conn.set_autocommit(True)
                yield conn

    @asynccontextmanager
    async def cursor(self, row_factory: Optional[RowFactory] = None) -> Iterator[AsyncCursor[Any]]:
        async with self.connection() as conn:
            async with conn.cursor(row_factory=row_factory) as cur:
                yield cur

    async def execute(
        self,
        query: Query,
        params: Optional[Parameters] = None,
    ):
        async with self.cursor() as cur:
            await cur.execute(query, params)

    async def query_one(
        self,
        query: Query,
        params: Optional[Parameters] = None,
    ) -> Optional[Row]:
        async with self.cursor(row_factory=dict_row) as cur:
            await cur.execute(query, params)
            return await cur.fetchone()

    async def query(
        self,
        query: Query,
        params: Optional[Parameters] = None,
    ) -> Sequence[Row]:
        async with self.cursor(row_factory=dict_row) as cur:
            await cur.execute(query, params)
            return await cur.fetchall()


@attr.frozen(kw_only=True)
class AsyncTransactionManager:
    _db: AsyncDatabase

    @asynccontextmanager
    async def transaction(
        self,
        savepoint_name: Optional[str] = None,
        force_rollback: bool = False,
    ) -> Iterator[AsyncTransaction]:
        async with self._db.connection() as conn:
            async with conn.transaction(savepoint_name, force_rollback) as tx:
                try:
                    token = _txn.set(tx)
                    yield tx
                finally:
                    _txn.reset(token)
