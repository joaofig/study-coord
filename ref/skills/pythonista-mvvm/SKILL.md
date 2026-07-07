---
name: pythonista-mvvm
description: Use when creating or modifying Models, Repositories, ViewModels, Views, or Dialogs. Triggers on "pattern", "mvvm", "model", "repository", "viewmodel", "view", "dialog", "crud", "save", "load", "sql".
---

# MVVM Pattern Implementation Guide

This skill provides instructions on how to effectively implement the MVVM (Model-View-ViewModel) pattern in this project, ensuring consistency across all entities.

## Core Layers

1.  **SQL DML**: Raw SQL files located in `src/db/sql/<entity>/`.
2.  **Repository**: Data access layer in `src/db/repository/` using `SQLCache` and `asyncio.to_thread`.
3.  **Model**: Dataclasses in `src/models/` representing data and business logic.
4.  **ViewModel**: Logic layer in `src/viewmodels/` managing state and UI interaction.
5.  **View**: UI layer in `src/views/` using NiceGUI, built on the `View` base class.

## Key Principles

-   **Separation of Concerns**: Keep UI logic in Views, coordination logic in ViewModels, and data logic in Models.
-   **Async First**: All IO operations (database, API) must be async or run in a thread via `asyncio.to_thread`.
-   **Messaging**: Use the `messenger` tool for inter-ViewModel communication (broadcast/subscribe).
-   **Data Binding**: Use NiceGUI's `bind_value`, `bind_enabled`, and `bind_visibility` to sync UI with ViewModels.

## Implementation Checklists

### New Entity Checklist
- [ ] Create SQL DML files (`save.sql`, `update.sql`, `delete.sql`, `get_by_id.sql`, `get_by_*.sql`).
- [ ] Create `<Entity>Repository.py`.
- [ ] Create `<entity>.py` model with `Entity` and `EntityList` classes.
- [ ] Update `src/models/__init__.py`.
- [ ] Create `<Entity>ViewModel.py` and `<Entity>ListViewModel.py`.
- [ ] Update `src/viewmodels/__init__.py`.
- [ ] Create `<Entity>Dialog.py`, `<Entity>Grid.py`, and `<Entity>Panel.py`.

## Reference Files

- [references/sql-dml.md](references/sql-dml.md) - SQL style and file organization.
- [references/models-repositories.md](references/models-repositories.md) - Implementation of Models and Repositories.
- [references/viewmodels.md](references/viewmodels.md) - ViewModel structure and data binding.
- [references/views-dialogs.md](references/views-dialogs.md) - NiceGUI View, Grid, and Dialog patterns.

## Related Skills

- [/pythonista-nicegui](../pythonista-nicegui/SKILL.md) - NiceGUI styling and component best practices.
- [/pythonista-patterning](../../../.agents/skills/pythonista-patterning/SKILL.md) - General code reuse patterns.
