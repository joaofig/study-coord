from typing import Any, LiteralString, cast

from psycopg import AsyncConnection

from src.repositories.postgres.base import PostgresCentral
from src.tools.observability import GridList
from src.viewmodels import ViewModel


async def run_query(query: str) -> list[dict[str, Any]]:
    """Executes a database query and returns fetched records asynchronously"""
    conn = await PostgresCentral().connect()
    if conn:
        async with conn.cursor() as cur:
            await cur.execute(cast(LiteralString, query))
            return await cur.fetchall()
    return []


class SQLViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.query: str = ""
        self.result = GridList()
        self.conn: AsyncConnection | None = None

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "run":
                query = kwargs.get("query", "")
                result = await run_query(query)
                self.result.replace(result)