from typing import Any, LiteralString, cast

from nicegui import binding
from psycopg import AsyncConnection, Column
from psycopg.errors import Error
from src.repositories.postgres.base import PostgresCentral
from nicemvvm.tools.observability import GridList
from nicemvvm.viewmodels.view_model import ViewModel


async def run_query(query: str) -> tuple[list[dict[str, Any]], list[Column] | None]:
    """Executes a database query and returns fetched records asynchronously"""
    conn = await PostgresCentral().connect()
    if conn:
        async with conn.cursor() as cur:
            await cur.execute(cast(LiteralString, query))
            return await cur.fetchall(), cur.description
    return [], []


@binding.bindable_dataclass
class SQLViewModel(ViewModel):
    query: str = ""
    result = GridList()
    schema: list[Column] | None = None
    conn: AsyncConnection | None = None
    messages: str = ""

    def __post_init__(self):
        super().__init__()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "run":
                query = kwargs.get("query", "")

                conn = await PostgresCentral().connect()
                if conn:
                    try:
                        async with conn.cursor() as cur:
                            await cur.execute(cast(LiteralString, query))
                            result = await cur.fetchall()
                            schema = cur.description
                            self.result.replace(result)
                            self.schema = schema
                            self.messages = ""
                    except Error as e:
                        self.result.clear()
                        if self.schema:
                            self.schema.clear()
                        self.messages = str(e)
                    finally:
                        await cur.close()
                        await conn.close()
