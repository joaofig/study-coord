from src.repositories.postgres.client import get_postgres_client
from src.tools import singleton
from psycopg import AsyncConnection, rows

@singleton
class PostgresCentral:
    conn: AsyncConnection | None = None

    async def connect(self) -> AsyncConnection | None:
        if not self.conn or self.conn.closed:
            self.conn = await get_postgres_client()
            # Set row factory to dict_row to match Supabase's dictionary-based results
            self.conn.row_factory = rows.dict_row
        return self.conn


class PostgresRepository:
    def __init__(self):
        self.conn: AsyncConnection | None = None

    async def connect(self) -> AsyncConnection | None:
        self.conn = await PostgresCentral().connect()
        return self.conn

    async def execute_query(self, sql: str, params: tuple | list | None = None) -> list[dict]:
        await self.connect()
        if self.conn:
            async with self.conn.cursor() as cur:
                await cur.execute(sql, params)
                if sql.strip().upper().startswith("SELECT") or "RETURNING" in sql.upper():
                    return await cur.fetchall()
                await self.conn.commit()
        return []

    async def insert_or_update(self, table: str, value: dict) -> dict:
        await self.connect()
        if self.conn:
            row_id_fields = [k for k in value if k == "id" or k.endswith("_id")]
            if not row_id_fields:
                # Fallback if no obvious ID field
                row_id = "id"
            else:
                row_id = row_id_fields[0]
                
            async with self.conn.cursor() as cur:
                if value.get(row_id, 0) > 0:
                    # UPDATE
                    cols = [k for k in value if k != row_id]
                    set_clause = ", ".join([f"{k} = %s" for k in cols])
                    values = [value[k] for k in cols] + [value[row_id]]
                    sql = f'UPDATE "{table}" SET {set_clause} WHERE {row_id} = %s'
                    await cur.execute(sql, values)
                    await self.conn.commit()
                    return value
                else:
                    # INSERT
                    val_copy = value.copy()
                    if row_id in val_copy:
                        del val_copy[row_id]
                    cols = list(val_copy.keys())
                    placeholders = ", ".join(["%s"] * len(cols))
                    sql = f'INSERT INTO "{table}" ({", ".join(cols)}) VALUES ({placeholders}) RETURNING *'
                    await cur.execute(sql, list(val_copy.values()))
                    result = await cur.fetchone()
                    await self.conn.commit()
                    return result if result else {}
        return {}
