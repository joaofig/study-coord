---
name: mvvm-view
description: Use when creating or modifying views (composite master views, tabbed detail panels, context-aware child panels, dashboard views, or any class derived from View) in NiceGUI MVVM architecture given a ViewModel. Triggers on "mvvm-view", "View", "View class", "master view", "panel view", "composite view", "detail panel", "StudyView", "StudyPanel", "view pattern".
writes-artifact: false
---

# NiceGUI MVVM View Pattern

This skill provides comprehensive instructions, blueprints, and guidelines for implementing View and Panel components in this NiceGUI MVVM project, connecting UI presentation layouts directly to ViewModels.

## Core Architecture & Principles

Views reside in `app/src/views/` (e.g., `app/src/views/study/study_view.py`, `app/src/views/study/patient_panel.py`, `app/src/views/admin/user_view.py`) and act as the visual presentation and layout coordination layer.

- **Base Class**: All views inherit from `View` (`nicemvvm.views.view.View`), receiving an injected `ViewModel` instance (`self.vm`).
- **Separation of Concerns**:
  - Views construct NiceGUI UI hierarchies (`ui.splitter`, `ui.tabs`, `ui.row`, `ui.column`, buttons, tooltips).
  - Views never execute SQL queries, database calls, or domain calculations directly; all actions are dispatched to the `ViewModel`.
- **ViewModel Interaction**:
  - Commands / Actions: Dispatched via `await self.vm.call("command_name", **kwargs)` (e.g., `"load"`, `"delete"`, `"save"`).
  - State Access: Retrieved via `self.vm.get("property_name")` and updated via `self.vm.set("property_name", value)`.
  - Reactive Bindings: Bound via `.bind_value(self.vm, ...)`, `.bind_enabled(self.vm, "selected_id")`, `.bind_visibility(self.vm, "selected_id")`, and `.bind_text_from(self.vm, ...)`.
- **Messenger Bus Integration**:
  - Context-aware child panels subscribe to parent lifecycle events in `__init__` via `self.subscribe(channel, message, handler)`.
  - Views trigger broad UI refreshes across sibling or parent components via `await self.broadcast(channel, message, **kwargs)`.
- **Authorization & Security**:
  - Mutating actions (Add, Edit, Delete, Export) must enforce permissions using `is_user_readonly()` from `nicemvvm.tools.user`.
  - Action buttons use `.set_enabled(not is_user_readonly())`.
  - Deletion methods check `if is_user_readonly():` and display negative notifications.
- **Action Toolbars & Dialog Workflows**:
  - Compact vertical toolbar on the left of grids with standard icons (`add`, `delete`, `table_view`).
  - Delete actions prompt confirmation via `DeleteWarningDialog`.
  - Add/Edit actions launch modal entity dialogs inheriting from `View` (see `mvvm-dialog` skill).

---

## View Taxonomy & Layout Types

| View Type | Typical File Name | Primary Layout | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Composite / Master View** | `<entity>_view.py` | `ui.splitter(horizontal=True, value=35)` | Hosts entity toolbar + AgGrid in the primary pane; hosts `<Entity>Panel` in the secondary pane. |
| **Tabbed Detail Panel** | `<entity>_panel.py` | `ui.tabs()` + `ui.tab_panels()` | Hosts related child entity panels under tabs; visibility bound to parent `selected_id`. |
| **Context-Aware Child Panel** | `<child>_panel.py` | `ui.row()` with toolbar + Grid | Subscribes to parent selection events (`"selected"`), manages parent foreign key context, launches scoped entity dialogs. |
| **Dashboard / Metric View** | `report_view.py` | Cards row + Filter selectors | Displays KPI metric cards bound to VM summary properties; filters detail metrics via dropdowns. |
| **Specialized Admin / Tool View** | `sql_view.py`, `settings_view.py` | Splitter / Custom controls | Hosts code editors (`ui.codemirror`), key bindings (`map_key`), reactive tab switching, and log consoles. |

---

## 1. Composite / Master View Blueprint (`<Entity>View`)

Used as the primary top-level view for a domain entity (e.g., Studies, Researchers, Users), organizing an entity grid and its corresponding detail panel within a horizontal splitter.

Create at `app/src/views/<module>/<entity>_view.py`:

```python
# src/views/study/entity_view.py
from nicegui import ui
from nicemvvm.tools.excel import export_to_excel
from nicemvvm.tools.user import get_user_name, is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View
from src.viewmodels import EntityViewModel
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.entity_dialog import EntityDialog
from src.views.study.entity_grid import EntityGrid
from src.views.study.entity_panel import EntityPanel


class EntityView(View):
    """
    Main composite view for Entity management.
    Coordinates the EntityGrid, action toolbar, and child EntityPanel.
    """

    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.splitter(horizontal=True, value=35).classes("w-full h-full") as splitter:
            with splitter.before, ui.row().classes("w-full h-full"):
                # Left compact action toolbar
                with ui.column().classes("h-full flex-none pl-0"):
                    with (
                        ui.button(icon="add", on_click=self._new_entity_dialog)
                        .classes("text-xs")
                        .props("padding=xs")
                        .set_enabled(not is_user_readonly())
                    ):
                        ui.tooltip("Add Entity")

                    with (
                        ui.button(icon="delete", on_click=self._on_delete_entity)
                        .bind_enabled(self.vm, "selected_id")
                        .classes("text-xs")
                        .props("color=red padding=xs")
                    ):
                        ui.tooltip("Delete Entity")

                    with (
                        ui.button(icon="table_view", on_click=self._on_export_to_excel)
                        .classes("text-xs")
                        .props("padding=xs")
                        .set_enabled(not is_user_readonly())
                    ):
                        ui.tooltip("Export to Excel")

                # Main entity tabular grid
                with ui.column().classes("h-full flex-1"):
                    EntityGrid(self.vm)

            # Detail container panel
            with splitter.after:
                EntityPanel(self.vm)

    async def _new_entity_dialog(self):
        """Open modal dialog to create a new entity."""
        entity_vm = EntityViewModel()
        entity_vm.created_by = get_user_name()
        entity_vm.updated_by = get_user_name()
        dialog = EntityDialog(entity_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    async def _on_delete_entity(self):
        """Prompt confirmation and delete the selected entity."""
        if is_user_readonly():
            ui.notification("You do not have permission to delete entities.", type="negative")
            return

        dialog = DeleteWarningDialog("Are you sure you want to delete this entity?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            entity_id = self.vm.get("selected_id")
            if entity_id:
                await self.vm.call("delete", entity_id=entity_id)

    def _on_export_to_excel(self):
        """Export current entity list to an Excel spreadsheet."""
        entities = self.vm.get("entities")
        if entities:
            export_to_excel(entities, filename="entities.xlsx")
```

---

## 2. Tabbed Detail Container Panel Blueprint (`<Entity>Panel`)

Used for organizing child entities and detail sub-panels under tabs, automatically synchronizing visibility with the parent selection.

Create at `app/src/views/<module>/<entity>_panel.py`:

```python
# src/views/study/entity_panel.py
from nicegui import ui
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View
from src.viewmodels import (
    ChildAListViewModel,
    ChildBListViewModel,
)
from src.views.study.child_a_panel import ChildAPanel
from src.views.study.child_b_panel import ChildBPanel


class EntityPanel(View):
    """
    Tabbed detail panel displaying child entities associated with the selected parent.
    Visibility is bound to the parent ViewModel's selected_id.
    """

    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with (
            ui.tabs()
            .props("dense no-caps")
            .bind_visibility(self.vm, "selected_id") as tabs
        ):
            tab_a = ui.tab("Children A").classes("text-sky-800")
            tab_b = ui.tab("Children B").classes("text-sky-800")

        with ui.tab_panels(tabs, value=tab_a, animated=False).classes("w-full h-full"):
            with (
                ui.tab_panel(tab_a)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                ChildAPanel(ChildAListViewModel())

            with (
                ui.tab_panel(tab_b)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                ChildBPanel(ChildBListViewModel())
```

---

## 3. Context-Aware Child Panel Blueprint (`<ChildEntity>Panel`)

Used for managing child entity collections dependent on a parent entity selection (e.g., Patients, Visits, Adverse Events in a Study).

Create at `app/src/views/<module>/<child_entity>_panel.py`:

```python
# src/views/study/child_a_panel.py
from datetime import datetime
from nicegui import app, ui
from nicemvvm.tools.excel import export_to_excel
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View
from src.viewmodels import ChildAViewModel
from src.views.dialogs.child_a_dialog import ChildADialog
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.study.child_a_grid import ChildAGrid


class ChildAPanel(View):
    """
    Child panel managing secondary entities scoped to a parent entity.
    Subscribes to parent selection events to update its local foreign key context.
    """

    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.parent_id: int = 0

        # Subscribe to parent entity selection events
        self.subscribe(
            channel="parent_entity",
            message="selected",
            handler=self._on_parent_selected,
        )

        with ui.row().classes("w-full h-full"):
            # Action toolbar
            with ui.column().classes("h-full flex-none pl-0"):
                with (
                    ui.button(icon="add", on_click=self._new_child_dialog)
                    .classes("text-xs")
                    .props("padding=xs")
                    .set_enabled(not is_user_readonly())
                ):
                    ui.tooltip("Add Child")

                with (
                    ui.button(icon="delete", on_click=self._on_delete_child)
                    .bind_enabled(self.vm, "selected_id")
                    .classes("text-xs")
                    .props("color=red padding=xs")
                ):
                    ui.tooltip("Delete Child")

                with (
                    ui.button(icon="table_view", on_click=self._on_export_to_excel)
                    .classes("text-xs")
                    .props("padding=xs")
                    .set_enabled(not is_user_readonly())
                ):
                    ui.tooltip("Export to Excel")

            # Tabular Grid
            with ui.column().classes("h-full flex-1"):
                ChildAGrid(self.vm)

    async def _on_parent_selected(self, **kwargs):
        """Update local foreign key context when parent selection changes."""
        if "parent_id" in kwargs:
            self.parent_id = kwargs["parent_id"]

    async def _new_child_dialog(self):
        """Launch creation dialog pre-populated with parent foreign key and audit data."""
        child_vm = ChildAViewModel()
        user_name = app.storage.user.get("username", "Unknown")
        child_vm.created_by = user_name
        child_vm.updated_by = user_name
        child_vm.created_at = datetime.now()
        child_vm.updated_at = datetime.now()
        child_vm.parent_id = self.parent_id

        dialog = ChildADialog(child_vm)
        result = await dialog.show()
        if result == "save":
            # Refresh local grid and notify parent list to update counts/status
            await self.vm.call("load", parent_id=self.parent_id)
            await self.broadcast("parent_list", "load")

    async def _on_delete_child(self):
        """Confirm and delete selected child entity."""
        if is_user_readonly():
            ui.notification("You do not have permission to delete this item.", type="negative")
            return

        dialog = DeleteWarningDialog("Are you sure you want to delete this record?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            selected_id = self.vm.get("selected_id")
            if selected_id:
                await self.vm.call("delete", child_id=selected_id)
                await self.vm.call("load", parent_id=self.parent_id)
                await self.broadcast("parent_list", "load")

    def _on_export_to_excel(self):
        """Export child records to Excel."""
        items = self.vm.get("items")
        if items:
            export_to_excel(items, filename="child_items.xlsx")
```

---

## 4. Dashboard / KPI Summary View Blueprint (`ReportView`)

Used for aggregate metrics, statistics cards, and dynamic filter controls.

Create at `app/src/views/report_view.py`:

```python
# src/views/report_view.py
from nicegui import ui
from nicegui.observables import ObservableDict
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


class ReportView(View):
    """
    Dashboard reporting view with reactive metric cards and study filtering.
    """

    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.studies = vm.get("studies")
        if isinstance(self.studies, ObservableDict):
            self.studies.on_change(self._update_selector)

        # Global KPI count cards
        with ui.row().classes("w-full"):
            self._add_count_card("Total Studies", "study_count")
            self._add_count_card("Total Patients", "patient_count")
            self._add_count_card("Total Researchers", "researcher_count")
            self._add_count_card("Total Visits", "visit_count")

        # Entity selector filter
        with ui.row().classes("w-full"):
            ui.separator()
            self.selector = (
                ui.select(self.studies, label="Select Study", on_change=self._on_study_change)
                .bind_value(self.vm, "study_id")
                .classes("w-100")
            )

        # Scoped detail metric cards
        with ui.row().classes("w-full"):
            self._add_count_card("Study Patients", "study_patient_count")
            self._add_count_card("Study Researchers", "study_researcher_count")
            self._add_count_card("Study Visits", "study_visit_count")

    def _add_count_card(self, title: str, property_name: str):
        """Construct a standardized metric KPI card bound to ViewModel property."""
        with ui.card().classes("bg-gray-200"):
            ui.label(title).classes("text-2xl")
            with ui.card_section().classes("w-full"):
                ui.label("0").bind_text_from(self.vm, property_name).classes(
                    "text-xl text-right font-bold text-sky-800"
                )

    async def _on_study_change(self):
        await self.vm.call("load_detail")

    def _update_selector(self, **kwargs):
        self.selector.set_options(self.studies)
```

---

## Common UI Patterns & Idioms

### 1. Standard Action Toolbar
Always structure toolbar action buttons with uniform styles and tooltips:
- Compact styling: `.classes("text-xs").props("padding=xs")`
- Delete button styling: `.props("color=red padding=xs")`
- Enablement bindings:
  - Add / Export: `.set_enabled(not is_user_readonly())`
  - Delete: `.bind_enabled(self.vm, "selected_id")`
- Tooltips: Place `ui.tooltip("...")` inside the `with ui.button(...):` context.

### 2. Safe Deletion Workflow
Destructive operations must always follow this sequence:
1. Verify permissions: Check `is_user_readonly()` first and notify with `type="negative"`.
2. Present modal confirmation: Instantiate `DeleteWarningDialog` and await `dialog.show()`.
3. If confirmed (`result == "delete"`):
   - Close dialog (`dialog.close()`).
   - Retrieve ID from VM (`self.vm.get("selected_id")`).
   - Call delete command: `await self.vm.call("delete", ...)`
   - Broadcast parent list refresh if necessary (`await self.broadcast("<channel>_list", "load")`).

### 3. Excel Export Workflow
Export data cleanly using `nicemvvm.tools.excel.export_to_excel`:
```python
def _on_export_to_excel(self):
    items = self.vm.get("<collection_name>")
    if items:
        # If items is a list of DTOs, serialize first: [i.to_dict() for i in items]
        export_to_excel(items, filename="<entities>.xlsx")
```

### 4. Dialog Launching & Result Lifecycle
When launching single-record creation/editing dialogs:
1. Instantiate single-entity ViewModel (e.g., `vm = EntityViewModel()`).
2. Populate audit metadata (`get_user_name()` / `app.storage.user.get("username")`) and foreign key context.
3. Instantiate `<Entity>Dialog(vm)`.
4. Await user completion: `result = await dialog.show()`.
5. On `"save"`, reload the list ViewModel: `await self.vm.call("load")`.

### 5. Splitters and Tab Styling
- Master-detail splitters: `ui.splitter(horizontal=True, value=35).classes("w-full h-full")`
- Detail tabs: `ui.tabs().props("dense no-caps").bind_visibility(self.vm, "selected_id")`
- Tab labels: `ui.tab("Title").classes("text-sky-800")`
- Tab panels container: `ui.tab_panels(tabs, value=first_tab, animated=False).classes("w-full h-full")`
- Panel zero padding: `ui.tab_panel(...).classes("pl-0 pt-0 pb-0 pr-0")`

---

## Application Entry Point Integration

In `app/src/views/main.py`, mount views using asynchronous loader functions:

```python
# src/views/main.py
async def study_view():
    from src.viewmodels import StudyListViewModel
    from src.views.study.study_view import StudyView

    study_vm = StudyListViewModel()
    await study_vm.call("load")
    StudyView(study_vm)
```

For non-async views requiring background data loading, use `ManagedTasks`:
```python
vm = UserListViewModel()
UserView(vm)
ManagedTasks().create(vm.call("load"))
```

---

## Package Export Conventions

Always export views in their module `__init__.py` (e.g. `src/views/__init__.py`) when applicable:

```python
# src/views/__init__.py
from .study_view import StudyView as StudyView
from .study_panel import StudyPanel as StudyPanel

__all__ = [
    "StudyView",
    "StudyPanel",
]
```

---

## Best Practices & Anti-Patterns

1. **No Database or Model Imports**: Views must NEVER import `src.repositories` or `src.models`. Views interact solely with ViewModels.
2. **Do Not Implement Business Rules in Views**: Validation rules, data parsing, and domain calculations belong in ViewModels and Models.
3. **Always Check Readonly Status**: Guard all create, update, and delete actions against readonly users with `is_user_readonly()`.
4. **Always Use Tooltips**: Every icon button in toolbars must have a descriptive `ui.tooltip`.
5. **Clean Zero-Padding on Tab Panels**: Add `.classes("pl-0 pt-0 pb-0 pr-0")` to `ui.tab_panel` so child grids and splitters align flush with container edges.
6. **Use Specific ViewModel Commands**: Dispatch named actions using `self.vm.call("<command>", **kwargs)` rather than manually mutating ViewModel internal state.

---

## Checklists

### Master View Checklist
- [ ] Inherits from `View` (`nicemvvm.views.view.View`)
- [ ] Accepts `vm: ViewModel` and calls `super().__init__(vm)`
- [ ] Configures `ui.splitter(horizontal=True, value=35)`
- [ ] Action toolbar includes Add, Delete, and Export to Excel buttons
- [ ] Buttons styled with `.classes("text-xs").props("padding=xs")` and tooltips
- [ ] Add button checks `.set_enabled(not is_user_readonly())`
- [ ] Delete button binds enabled state with `.bind_enabled(self.vm, "selected_id")` and confirms via `DeleteWarningDialog`
- [ ] Instantiates `<Entity>Grid(self.vm)` in primary splitter pane
- [ ] Instantiates `<Entity>Panel(self.vm)` in secondary splitter pane

### Tabbed / Child Panel Checklist
- [ ] Inherits from `View`
- [ ] Calls `super().__init__(vm)`
- [ ] Tabs bind visibility to parent `selected_id` using `.bind_visibility(self.vm, "selected_id")`
- [ ] Subscribes to parent selection events via `self.subscribe("parent", "selected", handler)`
- [ ] Updates local foreign key context (e.g. `self.parent_id`) on selection events
- [ ] Scoped Add action populates `parent_id` and audit fields before showing Dialog
- [ ] Scoped Delete action checks `is_user_readonly()`, prompts `DeleteWarningDialog`, deletes item, and reloads list
- [ ] Tab panels styled with `.classes("pl-0 pt-0 pb-0 pr-0")`
