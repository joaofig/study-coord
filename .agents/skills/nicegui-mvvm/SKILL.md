---
name: nicegui-mvvm
description: Use when writing NiceGUI applications using the MVVM pattern. Triggers on "mvvm", "nicegui mvvm", "architecture", "data flow".
---

# NiceGUI MVVM Architecture Guide

This skill provides an overview of the Model-View-ViewModel (MVVM) architecture implemented in this project, outlining layer responsibilities, data flow, and specialized skills for each component.

## Architecture Layers & Data Flow

```text
       ┌───────────────┐
       │     View      │ (NiceGUI UI components, inputs, buttons, AgGrid)
       └───────▲───────┘
               │ Data Binding / _on_call
       ┌───────▼───────┐
       │   ViewModel   │ (UI presentation state, validation, dirty tracking, GridList)
       └───────▲───────┘
               │ Typed DTOs
       ┌───────▼───────┐
       │     Model     │ (Domain services & business orchestration, no UI imports)
       └───────▲───────┘
               │ Typed DTOs / Dictionaries
       ┌───────▼───────┐
       │  Repository   │ (PostgresRepository with psycopg, SQL execution, row mapping)
       └───────────────┘
```

1. **DTO Layer (`src/dtos/`)**: Lightweight typed Pydantic models inheriting from `BaseDTO`. Provides serialization (`to_dict`) and deserialization (`from_dict`).
2. **Repository Layer (`src/repositories/postgres/`)**: Executes parameterized SQL via `PostgresRepository`, handles database CRUD operations, and maps rows to DTOs.
3. **Model Layer (`src/models/`)**: Domain services that orchestrate operations between ViewModels and Repositories. Pure Python domain logic with no UI framework dependencies.
4. **ViewModel Layer (`src/viewmodels/`)**: State containers and action dispatchers inheriting from `ViewModel`. Handles validation, reactive bindings, and inter-component messaging.
5. **View Layer (`src/views/`)**: Visual UI built with NiceGUI elements, binding directly to ViewModel properties.

---

## Dedicated MVVM Skills

For detailed patterns, blueprints, and checklists for each layer, refer to the corresponding dedicated skill:

- **[PostgreSQL Repository Skill](../mvvm-postgres-repository/SKILL.md)**: Data access layer, SQL queries, parameterized statements, and DTO mapping.
- **[Domain Model Skill](../mvvm-model/SKILL.md)**: Domain service orchestration, business rules, and multi-repository aggregation.
- **[ViewModel Skill](../mvvm-viewmodel/SKILL.md)**: Single record form ViewModels (`@binding.bindable_dataclass`) vs Plural list ViewModels (`GridList`).
- **[Dialog Skill](../mvvm-dialog/SKILL.md)**: Modal form views, validation banners, and action dialogs.
- **[Grid View Skill](../mvvm-grid-view/SKILL.md)**: Tabular data grid views (`ui.aggrid`) connected to list ViewModels, selection state, and row editing.
- **[NiceGUI AgGrid Skill](../nicegui-aggrid/SKILL.md)**: Data grid components backed by ViewModels using `ui.aggrid`.
