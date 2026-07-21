# Models and Repositories

This project uses a clean separation between data access (Repository) and domain logic (Model).

## Repositories

Repositories are responsible for executing SQL and mapping results to dictionaries. They are located in `src/db/repository/`.

-   Use `SQLCache` to load SQL files.
-   Use `get_connection()` for database access.
-   Map rows to dictionaries in `row_factory` or manually.
-   Expose `async` methods that use `asyncio.to_thread` for blocking DB calls.

### Repository Pattern

```python
class EntityRepository:
    def __init__(self):
        self.cache = SQLCache()

    def _get_by_id(self, entity_id: int) -> dict | None:
        conn = get_connection()
        conn.row_factory = lambda _, row: {...}
        cursor = conn.execute(self.cache.load("entity/get_by_id.sql"), (entity_id,))
        return cursor.fetchone()

    async def get(self, entity_id: int) -> dict | None:
        return await asyncio.to_thread(self._get_by_id, entity_id)
```

## Models

Models are located in `src/models/`. They are typically `dataclasses`.

### Single Entity Model

-   Implement `to_dict()` for serialization.
-   Implement `save()` which uses the Repository.
-   Implement `load(id)` as a class method or static method.

```python
@dataclass
class Entity:
    id: int = 0
    # ... fields ...

    def to_dict(self) -> dict:
        return { ... }

    async def save(self):
        repo = EntityRepository()
        data = await repo.save(self.to_dict())
        self.id = data["id"]
```

### List Model (Container)

Used to manage collections of entities.

```python
class EntityList:
    entities: list[Entity] = []

    async def load_from_parent(self, parent_id: int) -> list[Entity]:
        repo = EntityRepository()
        dicts = await repo.get_by_parent_id(parent_id)
        self.entities = [Entity(**d) for d in dicts]
        return self.entities

    @classmethod
    async def delete(cls, entity_id: int):
        repo = EntityRepository()
        await repo.delete(entity_id)
```
