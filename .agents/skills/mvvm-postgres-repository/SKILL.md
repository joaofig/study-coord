---
name: mvvm-postgres-repository
description: Use when creating or modifying PostgreSQL repository classes in the data access layer given a DTO. Triggers on "postgres repository", "repository", "sql", "PostgresRepository", "data access", "database layer", "CRUD repository", "insert_or_update", "execute_query".
---

# PostgreSQL Repository Pattern

This skill provides comprehensive instructions and patterns for implementing PostgreSQL repositories in this project, deriving the data access layer directly from a generic DTO (Data Transfer Object).

## Core Architecture & Principles

Repositories represent the data access layer (`app/src/repositories/postgres/`). They are responsible for executing SQL queries against the database and converting database dictionary rows into DTOs.

- **Base Class**: All PostgreSQL repositories inherit from `PostgresRepository` (`src.repositories.postgres.base`).
- **Connection Management**: Managed asynchronously by `PostgresCentral` singleton with `psycopg.AsyncConnection` and `rows.dict_row`.
- **SQL Execution**:
  - `execute_query(sql: LiteralString, params: tuple | list | None = None) -> list[dict]`: Executes parameterized SQL and returns dictionary records.
  - `insert_or_update(insert: LiteralString, update: LiteralString, value: dict) -> dict`: Inspects the primary key field in `value` (e.g. `entity_id > 0` or `id > 0`) to execute either the UPDATE or INSERT statement.
- **DTO Mapping**:
  - Reads map raw database records into DTOs using `DTO.from_dict(row)`.
  - Writes serialize DTOs to dictionaries using `dto.to_dict()`.
- **Safety & Typing**:
  - Always type SQL strings as `LiteralString` from `typing`.
  - Parameterize all dynamic inputs (`%s` for positional tuples in `execute_query`, `%(field_name)s` for named parameters in `insert_or_update`).
  - Quote SQL reserved keywords (e.g. `"number"`, `"order"`, `"user"`).

---

## Given a Generic DTO

Given a standard generic DTO inheriting from `BaseDTO`:

```python
# src/dtos/entity.py
from datetime import date, datetime
from typing import Self
from nicemvvm.tools.user import dict_to_date, dict_to_datetime, get_user_name
from src.dtos.base import BaseDTO


class EntityDTO(BaseDTO):
    entity_id: int = 0
    parent_id: int = 0
    code: str = ""
    name: str = ""
    status: str = "active"
    start_date: date = date.today()
    end_date: date | None = None
    comments: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            entity_id=data.get("entity_id", 0),
            parent_id=data.get("parent_id", 0),
            code=data.get("code", ""),
            name=data.get("name", ""),
            status=data.get("status", "active"),
            start_date=dict_to_date(data, "start_date") or date.today(),
            end_date=dict_to_date(data, "end_date", None),
            comments=data.get("comments", ""),
            created_at=dict_to_datetime(data, "created_at") or datetime.now(),
            created_by=data.get("created_by", get_user_name()),
            updated_at=dict_to_datetime(data, "updated_at") or datetime.now(),
            updated_by=data.get("updated_by", get_user_name()),
        )

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "parent_id": self.parent_id,
            "code": self.code,
            "name": self.name,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "comments": self.comments,
        } | super().to_dict()
```

---

## Repository Implementation Blueprint

Create the repository file at `app/src/repositories/postgres/<entity>.py`:

```python
# src/repositories/postgres/entity.py
import builtins
from typing import LiteralString

from src.dtos.entity import EntityDTO
from src.repositories.postgres.base import PostgresRepository


class EntityRepository(PostgresRepository):
    def __init__(self):
        super().__init__()

    async def load(self, entity_id: int) -> EntityDTO | None:
        """Fetch a single record by primary key."""
        sql: LiteralString = """
        SELECT  entity_id
        ,       parent_id
        ,       "code"
        ,       name
        ,       status
        ,       start_date
        ,       end_date
        ,       comments
        ,       created_at
        ,       created_by
        ,       updated_at
        ,       updated_by
        FROM    entity
        WHERE   entity_id = %s
        """
        result = await self.execute_query(sql, (entity_id,))
        if result:
            return EntityDTO.from_dict(result[0])
        return None

    async def list(self, parent_id: int = 0) -> builtins.list[EntityDTO]:
        """Fetch all records, optionally filtered by a parent foreign key."""
        if parent_id > 0:
            sql: LiteralString = """
            SELECT  entity_id, parent_id, "code", name, status, start_date, end_date,
                    comments, created_at, created_by, updated_at, updated_by
            FROM    entity
            WHERE   parent_id = %s
            ORDER BY entity_id
            """
            result = await self.execute_query(sql, (parent_id,))
        else:
            sql: LiteralString = """
            SELECT  entity_id, parent_id, "code", name, status, start_date, end_date,
                    comments, created_at, created_by, updated_at, updated_by
            FROM    entity
            ORDER BY entity_id
            """
            result = await self.execute_query(sql)

        return [EntityDTO.from_dict(row) for row in result]

    async def save(self, entity: EntityDTO) -> dict:
        """Insert or update a record using DTO dictionary mapping."""
        insert: LiteralString = """
        INSERT INTO entity (
            parent_id, "code", name, status, start_date, end_date, comments,
            created_at, created_by, updated_at, updated_by
        )
        VALUES (
            %(parent_id)s, %(code)s, %(name)s, %(status)s, %(start_date)s, %(end_date)s, %(comments)s,
            %(created_at)s, %(created_by)s, %(updated_at)s, %(updated_by)s
        )
        RETURNING entity_id
        """

        update: LiteralString = """
        UPDATE entity
        SET     parent_id = %(parent_id)s,
                "code" = %(code)s,
                name = %(name)s,
                status = %(status)s,
                start_date = %(start_date)s,
                end_date = %(end_date)s,
                comments = %(comments)s,
                created_at = %(created_at)s,
                created_by = %(created_by)s,
                updated_at = %(updated_at)s,
                updated_by = %(updated_by)s
        WHERE   entity_id = %(entity_id)s
        RETURNING entity_id
        """

        return await self.insert_or_update(insert, update, entity.to_dict())

    async def delete(self, *, entity_id: int = 0, parent_id: int = 0) -> None:
        """Delete it by primary key or by parent foreign key."""
        if parent_id:
            sql: LiteralString = "DELETE FROM entity WHERE parent_id = %s"
            await self.execute_query(sql, (parent_id,))
        elif entity_id:
            sql: LiteralString = "DELETE FROM entity WHERE entity_id = %s"
            await self.execute_query(sql, (entity_id,))

    async def code_exists(self, code: str, parent_id: int = 0) -> bool:
        """Check uniqueness / existence for an entity attribute."""
        if parent_id > 0:
            sql: LiteralString = """
            SELECT  entity_id
            FROM    entity
            WHERE   parent_id = %s AND "code" = %s
            """
            result = await self.execute_query(sql, (parent_id, code))
        else:
            sql: LiteralString = """
            SELECT  entity_id
            FROM    entity
            WHERE   "code" = %s
            """
            result = await self.execute_query(sql, (code,))
        return len(result) > 0
```

---

## Package Export Conventions

Always export the new repository in `src/repositories/postgres/__init__.py` and re-export in `src/repositories/__init__.py`:

```python
# src/repositories/postgres/__init__.py
from src.repositories.postgres.entity import EntityRepository

__all__ = [
    # ...
    "EntityRepository",
]
```

```python
# src/repositories/__init__.py
from src.repositories.postgres import EntityRepository

__all__ = [
    # ...
    "EntityRepository",
]
```

---

## Best Practices & Patterns

1. **Explicit Column Lists**: Never use `SELECT *`. Always list all columns explicitly in SELECT statements to guarantee positional and schema stability.
2. **Primary Key Conventions**: The primary key column must be named `<entity>_id` or `id` so `insert_or_update` automatically detects whether to INSERT or UPDATE.
3. **Audit Fields**: Ensure `created_at`, `created_by`, `updated_at`, and `updated_by` are always included in INSERT and UPDATE statements.
4. **Keyword Escaping**: Wrap reserved SQL keywords (such as `"number"`, `"order"`, `"user"`, `"group"`, `"code"`) in double quotes in SQL strings.
5. **Composed / View DTOs**: When displaying aggregated grid rows (e.g. counts of children), create a dedicated `<Entity>RowDTO` and write a custom SELECT query calculating aggregates in the repository.

---

## Checklist

- [ ] Repository inherits from `PostgresRepository`
- [ ] SQL queries use `LiteralString` typing
- [ ] Query parameters passed via tuples (`%s`) or dictionaries (`%(key)s`)
- [ ] `load` returns `DTO | None` using `DTO.from_dict`
- [ ] `list` returns `list[DTO]` using `[DTO.from_dict(row) for row in result]`
- [ ] `save` implements `RETURNING <entity>_id` on both INSERT and UPDATE queries and calls `insert_or_update`
- [ ] `delete` safely removes rows by primary key or parent foreign key
- [ ] Repository is exported in `src/repositories/postgres/__init__.py` and `src/repositories/__init__.py`
