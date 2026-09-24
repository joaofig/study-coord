---
name: model
description: Use when creating or modifying Model classes (domain service orchestrators) given a DTO. Triggers on "model", "domain model", "business logic", "service layer", "Model", "Model class", "orchestrator".
---

# Domain Model Pattern

This skill provides comprehensive instructions and patterns for implementing domain Models in this project, deriving the business logic and service orchestration layer directly from a generic DTO (Data Transfer Object).

## Core Architecture & Principles

Models represent the domain and orchestration layer (`app/src/models/`). They act as service layer orchestrators between the ViewModels (UI state) and Repositories (database access).

- **No UI Imports**: Models must NEVER import `nicegui` or any UI framework components. They are pure Python domain services.
- **DTOs as Data Contracts**: Models accept and return DTOs (`src/dtos/`), ensuring strict typing across application boundaries.
- **Encapsulation**: ViewModels communicate strictly with Models; ViewModels never directly invoke Repositories or SQL queries.
- **Domain Responsibilities**:
  - Orchestrating CRUD operations via the repository.
  - Ensuring business invariants, status lifecycle transitions, and uniqueness constraints.
  - Handling multi-repository operations or cross-entity aggregation.

---

## Given a Generic DTO

Given a standard generic DTO:

```python
# src/dtos/entity.py
from datetime import date, datetime
from typing import Self
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
    # from_dict and to_dict methods...
```

---

## Model Implementation Blueprint

Create the model file at `app/src/models/<entity>.py`:

```python
# src/models/entity.py
import builtins

from src.dtos.entity import EntityDTO
from src.repositories import EntityRepository


class EntityModel:
    repo = EntityRepository()

    async def save(self, dto: EntityDTO) -> EntityDTO:
        """
        Persist an entity (create or update) and return the updated DTO.
        Updates the primary key on the DTO if it was newly inserted.
        """
        result = await self.repo.save(dto)
        if result and "entity_id" in result:
            dto.entity_id = result["entity_id"]
        return dto

    async def load(self, entity_id: int) -> EntityDTO | None:
        """Load a single entity by primary key."""
        return await self.repo.load(entity_id)

    async def list(self, parent_id: int = 0) -> builtins.list[EntityDTO]:
        """List entities, optionally filtered by parent foreign key."""
        return await self.repo.list(parent_id)

    async def delete(self, entity_id: int) -> None:
        """Delete an entity by primary key."""
        await self.repo.delete(entity_id=entity_id)

    async def code_exists(self, code: str, parent_id: int = 0) -> bool:
        """Domain validation check: verify code uniqueness."""
        return await self.repo.code_exists(code, parent_id)
```

---

## Aggregator & Multi-Repository Models

When business logic requires coordinating multiple entities or computing aggregate summaries, create an aggregator Model:

```python
# src/models/entity_summary.py
import builtins
from src.dtos.entity import EntitySummaryDTO
from src.repositories import EntityRepository, ChildRepository, LogRepository


class EntitySummaryModel:
    entity_repo = EntityRepository()
    child_repo = ChildRepository()
    log_repo = LogRepository()

    async def get_summary(self, entity_id: int) -> EntitySummaryDTO | None:
        entity = await self.entity_repo.load(entity_id)
        if not entity:
            return None
        children = await self.child_repo.list(parent_id=entity_id)
        logs = await self.log_repo.list(entity_id=entity_id)
        return EntitySummaryDTO(
            entity=entity,
            child_count=len(children),
            recent_logs=logs[:5],
        )
```

---

## Package Export Conventions

Always export the new model in `src/models/__init__.py`:

```python
# src/models/__init__.py
from src.models.entity import EntityModel

__all__ = [
    # ...
    "EntityModel",
]
```

---

## Best Practices & Patterns

1. **Keep Models Thin but Responsible**: Move domain validation rules (e.g., uniqueness checks, status validations) and orchestration into the Model so they can be reused across different ViewModels and APIs.
2. **Accept and Return DTOs**: Always work with DTO instances (`EntityDTO`) rather than raw dictionaries or arbitrary tuples.
3. **No UI State in Models**: Never store active UI selections, form validation messages, or UI notifications in Models. UI state belongs strictly in ViewModels.
4. **Idempotent Operations**: Ensure delete and status transitions handle non-existent entities gracefully without crashing.

---

## Checklist

- [ ] Model file created in `src/models/<entity>.py`
- [ ] No `nicegui` or UI-related imports
- [ ] Instantiates corresponding `EntityRepository`
- [ ] Implements async `save`, `load`, `list`, and `delete`
- [ ] Accepts and returns typed DTOs
- [ ] Provides domain validation helper methods (e.g. `code_exists`)
- [ ] Model is exported in `src/models/__init__.py`
