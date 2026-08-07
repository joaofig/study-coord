---
name: nicegui-aggrid
description: Use when building grid views using `ui.aggrid` in NiceGUI. Triggers on "grid", "table", "aggrid", "list view", or when creating a new data grid component.
---

# NiceGUI AgGrid Pattern

This skill provides the standard pattern for implementing data grids using `ui.aggrid` in this project, following the MVVM architecture.

## Core Pattern

All grid components should inherit from `View` and be backed by a `ViewModel`.

### 1. Initialization
- Subscribe to data changes in the `ViewModel`.
- Initialize the grid using `_build_grid()`.
- Register global event handlers (e.g., for row editing).

### 2. Grid Construction (`_build_grid`)
- Define columns in a `columns` list.
- Use `getRowId` to uniquely identify rows (crucial for row-level operations).
- Use `theme="balham"` and `.classes("w-full h-full")` for consistency.
- Handle `selectionChanged` to notify the `ViewModel`.

### 3. Data Updates (`_update_grid`)
- Update `rowData` in `grid.options` or use `run_grid_method("setGridOption", "rowData", ...)`.
- Restore selection if necessary.

### 4. Row Editing
- Use a custom `cellRenderer` for an "Edit" column that emits a global event.
- Listen for this event using `ui.on` and handle it in the view.

## Implementation Example

```python
from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.views.view import View

class EntityGrid(View):
    def __init__(self, vm):
        super().__init__(vm)
        self.data = self.vm.get("items")
        
        # Observe changes if using ObservableList
        if isinstance(self.data, ObservableList):
            self.data.on_change(self._update_grid)
            
        self.grid: AgGrid = self._build_grid()
        
        # Subscribe to save events to refresh data
        self.subscribe("entity", "saved", self._update_grid)

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "id",
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
            {"headerName": "Name", "field": "name", "sortable": True},
            # ... other columns
        ]
        
        grid_def = {
            "columnDefs": columns,
            "rowData": self.data,
            "rowSelection": {"mode": "singleRow"},
            ":getRowId": "(params) => String(params.data.id)",
        }
        
        ui.on("entity-row-edit", self._on_edit)
        
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda e: self._on_selection_changed(e))
        return grid

    async def _update_grid(self):
        # Update rowData and trigger grid update
        self.grid.options["rowData"] = self.vm.get("items")
        self.grid.update()
        
        # Alternative for partial updates:
        # await self.grid.run_grid_method("setGridOption", "rowData", self.vm.get("items"))

    async def _on_edit(self, event):
        row_data = event.args
        # Handle edit (e.g., open dialog)

    async def _on_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call("item_selected", item_id=row["id"])
```

## Best Practices
- **Row IDs**: Always use `:getRowId` to ensure AgGrid can track rows correctly during updates.
- **Observable Lists**: If the ViewModel uses `ObservableList`, bind `on_change` to `_update_grid`.
- **Messenger**: Use `self.subscribe` and `self.broadcast` for cross-component communication.
- **Styling**: Stick to `theme="balham"` and ensure the grid container has a height (e.g., `.classes("h-full")`).

## Checklist
- [ ] Inherits from `View`
- [ ] Uses `ViewModel` for data and actions
- [ ] Implements `_build_grid` with `getRowId`
- [ ] Uses `balham` theme and full size classes
- [ ] Handles selection changes
- [ ] Provides an edit mechanism if required
- [ ] Subscribes to relevant update messages
