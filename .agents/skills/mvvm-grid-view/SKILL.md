---
name: mvvm-grid-view
description: Use when creating or modifying grid views (AgGrid list views, table views, data grids) in NiceGUI MVVM architecture given a ViewModel. Triggers on "mvvm-grid-view", "grid view", "AgGrid", "data grid", "list view", "Grid", "View grid", "ui.aggrid", "grid pattern".
writes-artifact: false
---

# NiceGUI MVVM Grid View Pattern

This skill provides comprehensive instructions, blueprints, and guidelines for implementing data grid views using `ui.aggrid` in this NiceGUI MVVM project, connecting list/plural ViewModels to interactive, reactive tabular UI components.

## Core Architecture & Principles

Grid views reside in `app/src/views/<module>/` (e.g., `app/src/views/study/patient_grid.py`, `app/src/views/admin/user_grid.py`) and act as the tabular presentation layer for entity collections.

- **Base Class**: Grid views inherit from `View` (`nicemvvm.views.view.View`) and receive a plural list `ViewModel` (e.g., `PatientListViewModel`, `StudyListViewModel`).
- **Reactive Data Binding**:
  - The grid extracts the reactive collection from the ViewModel: `self.items = self.vm.get("<entities>")`.
  - If `self.items` is an `ObservableList`, registers `self.items.on_change(self._update_grid)` for automatic UI refreshes upon collection mutations.
- **AgGrid Construction (`_build_grid`)**:
  - Styled with `theme="balham"` and sized with `.classes("w-full h-full")`.
  - Configured with `rowSelection`: `{"mode": "singleRow", "checkboxes": False, "enableClickSelection": True}`.
  - **Crucial Row Identity**: Configured with `:getRowId: "(params) => String(params.data.<entity>_id)"` (or `selected_id`).
- **Action / Edit Column Renderer**:
  - Injects a custom JavaScript button cell renderer using `:cellRenderer` that calls `emitEvent('<entity>-row-edit', params.data)`.
  - Listens globally in NiceGUI with `ui.on("<entity>-row-edit", self._on_edit)`.
- **Dynamic Updates & Selection Retention**:
  - `_update_grid()` updates the grid row data via `await self.grid.run_grid_method("setGridOption", "rowData", self.items)`.
  - If the list becomes empty, calls `await self.grid.run_grid_method("redrawRows")` to clear stale rows.
  - Automatically restores previous row selection using `await self.grid.run_row_method(selected_id, "setSelected", True)`.
- **Row Selection Dispatch**:
  - Listens to AgGrid's `selectionChanged` event.
  - Queries `row = await self.grid.get_selected_row()`.
  - Dispatches `await self.vm.call("select", <entity>=row, <entity>_id=row["<entity>_id"])` (or `await self.vm.call("<entity>_selected", ...)`).
- **Edit Modal Lifecycle Integration**:
  - Opens the entity's modal dialog (`<Entity>Dialog`) backed by a new `<Entity>ViewModel` instance.
  - Sets user auditing (`updated_by = app.storage.user.get("username", "Unknown")`, `updated_at = datetime.now()`).
  - Reloads the list ViewModel upon successful save: `await self.vm.call("load")`.

---

## Standard Entity Grid Blueprint (`<Entity>Grid`)

Create the grid view file at `app/src/views/<module>/<entity>_grid.py`:

```python
# src/views/entity/entity_grid.py
import asyncio
from datetime import datetime

from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View
from src.viewmodels import EntityViewModel
from src.views.dialogs.entity_dialog import EntityDialog


class EntityGrid(View):
    def __init__(self, vm: ViewModel) -> None:
        super().__init__(vm)

        self.entities = self.vm.get("entities")
        if isinstance(self.entities, ObservableList):
            self.entities.on_change(self._update_grid)

        # Optional messenger subscription for cross-view synchronization
        self.subscribe("entity", "saved", self._update_grid)

        self.grid: AgGrid = self._build_grid()

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "entity_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('entity-row-edit', params.data);
                    });
                    return btn;
                }
                """,
            },
            {
                "headerName": "Code",
                "field": "code",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
                "cellStyle": {"fontWeight": "bold"},
            },
            {
                "headerName": "Name",
                "field": "name",
                "sortable": True,
                "align": "left",
                "flex": 1,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Start Date",
                "field": "start_date",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agDateColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Count",
                "field": "item_count",
                "sortable": True,
                "type": "numericColumn",
                "align": "right",
                "width": 90,
            },
            {
                "headerName": "Status",
                "field": "status",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
        ]

        grid_def = {
            "columnDefs": columns,
            "rowData": self.entities,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.entity_id)",
        }

        ui.on("entity-row-edit", self._handle_edit)

        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on(
            "selectionChanged",
            lambda event: asyncio.create_task(self._row_selection_changed(event)),
        )
        return grid

    async def _update_grid(self) -> None:
        """Update grid rows and restore selected state."""
        await self.grid.run_grid_method("setGridOption", "rowData", self.entities)

        if len(self.entities) == 0:
            await self.grid.run_grid_method("redrawRows")

        # Restore previously selected row if available
        selected_id = self.vm.get("selected_id")
        if selected_id and selected_id != 0:
            await self.grid.run_row_method(selected_id, "setSelected", True)

    async def _handle_edit(self, event) -> None:
        """Handle edit button event dispatched from AgGrid cellRenderer."""
        row_data = event.args
        if row_data:
            await self._edit_entity(row_data)

    async def _edit_entity(self, row_data: dict) -> None:
        """Open the entity edit dialog and refresh the list upon saving."""
        vm = EntityViewModel()
        vm.from_dict(row_data)
        vm.updated_by = app.storage.user.get("username", "Unknown")
        vm.updated_at = datetime.now()

        dialog = EntityDialog(vm=vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    async def _row_selection_changed(self, event) -> None:
        """Propagate row selection changes to the ViewModel."""
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call(
                "select",
                entity=row,
                entity_id=row["entity_id"],
            )
        else:
            await self.vm.call("unselect")

    def show(self) -> AgGrid:
        """Optional helper to return the underlying AgGrid element."""
        return self.grid
```

---

## Child / Master-Detail Grid Pattern (Context-Dependent)

When a grid renders entities subordinate to a parent (e.g., Visits or Adverse Events under a Study or Patient), parameterize the loading and editing methods with parent identifiers:

```python
# src/views/study/visit_grid.py
import asyncio
from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View
from src.viewmodels.study.visit import VisitViewModel
from src.views.dialogs.visit_dialog import StudyVisitDialog


class StudyVisitGrid(View):
    def __init__(self, vm: ViewModel) -> None:
        super().__init__(vm)

        self.visits = self.vm.get("visits")
        if isinstance(self.visits, ObservableList):
            self.visits.on_change(self._update_grid)

        self.subscribe("visit", "saved", self._update_grid)
        self.grid: AgGrid = self._build_grid()

    async def _edit_visit(self, visit_id: int) -> None:
        visit_vm = VisitViewModel()
        visit_vm.updated_by = app.storage.user.get("username", "Unknown")
        study_id = self.vm.get("study_id")

        # Load parent contextual entities needed by the dialog (e.g., patient selector)
        await visit_vm.call("load_patients", study_id=study_id)
        await visit_vm.call("load", visit_id=visit_id)

        dialog = StudyVisitDialog(visit_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=study_id)
            await self.broadcast("study_list", "load")

    async def _on_edit(self, event) -> None:
        row_data = event.args
        if row_data:
            await self._edit_visit(row_data["visit_id"])

    async def _update_grid(self) -> None:
        if len(self.visits) > 0:
            await self.grid.run_grid_method("setGridOption", "rowData", self.visits)
        else:
            await self.grid.run_grid_method("setGridOption", "rowData", [])

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "visit_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('visit-row-edit', params.data);
                    });
                    return btn;
                }
                """,
            },
            {
                "headerName": "Date",
                "field": "visit_date",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Type",
                "field": "visit_type",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.visits,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.visit_id)",
        }
        ui.on("visit-row-edit", self._on_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on(
            "selectionChanged",
            lambda event: asyncio.create_task(self._row_selection_changed(event)),
        )
        return grid

    async def _row_selection_changed(self, event) -> None:
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call("visit_selected", visit_id=row["visit_id"])
        else:
            await self.vm.call("visit_unselected")
```

---

## Column Definition Reference Guide

| Feature / Column Type | AgGrid Column Definition Configuration |
| :--- | :--- |
| **Edit Action Button** | `{"headerName": "Edit", "field": "<id_field>", "width": 50, ":cellRenderer": "(params) => { ... emitEvent('<event_name>', params.data); return btn; }"}` |
| **Primary Code / Key** | `{"headerName": "Code", "field": "code", "sortable": True, "align": "left", "width": 100, "cellStyle": {"fontWeight": "bold"}}` |
| **Text (Flex-width)** | `{"headerName": "Title", "field": "title", "sortable": True, "align": "left", "flex": 1, "filter": "agTextColumnFilter", "floatingFilter": False}` |
| **Numeric Count / Sum** | `{"headerName": "Visits", "field": "visits", "sortable": True, "type": "numericColumn", "align": "right", "width": 90}` |
| **Date Column** | `{"headerName": "Date", "field": "start_date", "sortable": True, "align": "left", "width": 120, "filter": "agDateColumnFilter"}` |
| **Filtered Text** | `{"headerName": "Status", "field": "status", "sortable": True, "align": "left", "filter": "agTextColumnFilter", "floatingFilter": False}` |

---

## Embedding Grids in Panels & Views

Grid views are usually hosted inside a container Panel view alongside action buttons (e.g., Create, Delete, Refresh):

```python
# src/views/entity/entity_panel.py
from nicegui import ui
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.views.view import View
from src.views.entity.entity_grid import EntityGrid


class EntityPanel(View):
    def _build_panel(self):
        with ui.row().classes("w-full h-full gap-2"):
            # Left: Full-size grid
            with ui.column().classes("flex-1 h-full"):
                EntityGrid(self.vm)

            # Right: Sidebar action controls
            with ui.column().classes("w-12 items-center gap-2 pt-2"):
                ui.button(
                    icon="add",
                    on_click=self._new_entity_dialog,
                ).props("round dense").tooltip("New Entity").set_enabled(
                    not is_user_readonly()
                )

                ui.button(
                    icon="delete",
                    on_click=self._on_delete_entity,
                ).props("round dense color=red").tooltip("Delete Entity").bind_enabled(
                    self.vm, "selected_id"
                )
```

---

## Package Export Conventions

Export the grid class in the module's `__init__.py`:

```python
# src/views/study/__init__.py
from .study_grid import StudyGrid as StudyGrid
from .patient_grid import StudyPatientGrid as StudyPatientGrid
from .visit_grid import StudyVisitGrid as StudyVisitGrid

__all__ = [
    "StudyGrid",
    "StudyPatientGrid",
    "StudyVisitGrid",
]
```

---

## Best Practices & Patterns

1. **Always Set `:getRowId`**: AgGrid requires unique row identity mapping via `:getRowId: "(params) => String(params.data.<id_field>)"` for reliable row updates, redraws, and selection tracking.
2. **Observe `ObservableList`**: Always check `isinstance(self.items, ObservableList)` and register `self.items.on_change(self._update_grid)` so changes made in ViewModels automatically refresh the table.
3. **Selection Retention**: In `_update_grid()`, query `self.vm.get("selected_id")` and call `await self.grid.run_row_method(selected_id, "setSelected", True)` to avoid losing user selection upon data reloads.
4. **Use `theme="balham"`**: Standardize styling across all grid components with `theme="balham"` and layout classes `.classes("w-full h-full")`.
5. **Decouple Event Emitting**: Use JS `emitEvent('<name>', params.data)` combined with `ui.on('<name>', ...)` to dispatch row edit actions cleanly without inline python closures.
6. **Messenger Integration**: Subscribe grid views to domain event topics (e.g., `self.subscribe("entity", "saved", self._update_grid)`) for instant synchronization across tab panels.

---

## Checklist

- [ ] Grid class inherits from `View` and accepts a plural list `ViewModel`
- [ ] Subscribes to `ObservableList` changes via `self.items.on_change(self._update_grid)`
- [ ] Configures `:getRowId` with unique record ID field in `grid_def`
- [ ] Sets `theme="balham"` and `.classes("w-full h-full")`
- [ ] Provides an Edit action column with JS `emitEvent` and registers `ui.on` handler
- [ ] Handles `selectionChanged` event and updates ViewModel via `self.vm.call("select", ...)`
- [ ] Implements `_update_grid()` using `run_grid_method("setGridOption", "rowData", ...)`
- [ ] Restores row selection in `_update_grid()` when `selected_id` is present
- [ ] Edit handler initializes `<Entity>ViewModel`, stamps user audit info, opens `<Entity>Dialog`, and reloads list on `"save"`
- [ ] Grid class exported in package `__init__.py`
