---
name: mvvm-dialog
description: Use when creating or modifying dialogs (modal forms, confirmation dialogs, detail editors) in NiceGUI MVVM architecture given a ViewModel. Triggers on "mvvm-dialog", "dialog", "modal", "Dialog", "View dialog", "DeleteWarningDialog", "ui.dialog", "dialog pattern".
writes-artifact: false
---

# NiceGUI MVVM Dialog Pattern

This skill provides comprehensive instructions, blueprints, and guidelines for implementing modal dialogs in this NiceGUI MVVM project, connecting UI dialog forms directly to single-entity ViewModels.

## Core Architecture & Principles

Dialogs reside in `app/src/views/dialogs/` and act as modal views for creating, editing, and validating entities or confirming critical user actions.

- **Base Class**: Entity dialogs inherit from `View` (`nicemvvm.views.view.View`), receiving a single-entity `ViewModel`.
- **Async Modal Lifecycle**:
  - Dialogs wrap NiceGUI's `with ui.dialog() as dialog:`.
  - `show(self)` is an async method returning `await self.dialog`, pausing caller execution until the user submits or closes the dialog.
  - User actions close the dialog and return a result string via `self.dialog.submit("save")` or `dialog.submit("close")`.
- **Two-Way Data Binding**: Form inputs bind directly to ViewModel properties via `.bind_value(self.vm, "property_name")`.
- **Validation Pipeline**:
  - Field-level validation: Provided via `validation=validate_func` on `ui.input` controls for immediate syntax/length feedback.
  - Domain-level validation: Dialog's `save` method invokes `await self.vm.call("validate")` and checks `self.vm.get("is_invalid")`.
  - Error Banner: `ui.markdown()` bound to `self.vm.validation` and visible only when `self.vm.is_invalid` is True.
- **Permission Enforcement**: Save buttons must check user privileges via `.set_enabled(not is_user_readonly())` from `nicemvvm.tools.user`.

---

## Standard Entity Dialog Blueprint (`<Entity>Dialog`)

Create the dialog file at `app/src/views/dialogs/<entity>_dialog.py`:

```python
# src/views/dialogs/entity_dialog.py
from nicegui import ui
from nicegui.elements.dialog import Dialog
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


def validate_code(value: str | None) -> str | None:
    """Field-level validator for immediate input feedback."""
    if not value or not value.strip():
        return "Code is required"
    if len(value) < 2:
        return "Code must be at least 2 characters long"
    return None


def validate_name(value: str | None) -> str | None:
    """Field-level validator for immediate input feedback."""
    if not value or not value.strip():
        return "Name is required"
    return None


class EntityDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.dialog: Dialog = self._build_dialog()

    async def show(self) -> str | None:
        """Display the modal dialog and await user submission."""
        return await self.dialog

    async def save(self) -> None:
        """Validate ViewModel domain rules and persist changes if valid."""
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")

    def _build_dialog(self) -> Dialog:
        # Standard card width: w-120 (single column) or w-240 / w-280 (two columns)
        with ui.dialog() as dialog, ui.card().classes("w-120"):
            # Header bar
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("Entity Details").classes("text-base font-semibold")

            # Form fields bound to ViewModel
            ui.input(
                label="Code",
                validation=validate_code,
            ).classes("w-full").props("dense").bind_value(self.vm, "code")

            ui.input(
                label="Name",
                validation=validate_name,
            ).classes("w-full").props("dense").bind_value(self.vm, "name")

            with ui.row().classes("w-full"):
                ui.date_input(
                    label="Start Date"
                ).classes("w-36").props("dense").bind_value(self.vm, "start_date")

                ui.date_input(
                    label="End Date"
                ).classes("w-36").props("clearable dense").bind_value(self.vm, "end_date")

            statuses = self.vm.get("statuses") or ["active", "inactive", "pending"]
            ui.select(
                options=statuses,
                label="Status",
            ).classes("w-full").props("dense").bind_value(self.vm, "status")

            ui.textarea(
                label="Comments"
            ).classes("w-full").props("dense").bind_value(self.vm, "comments")

            # Validation error banner (visible only when is_invalid is True)
            ui.markdown().classes("bg-orange-200 w-full p-2 rounded").bind_content_from(
                self.vm, "validation"
            ).bind_visibility_from(self.vm, "is_invalid")

            # Action buttons
            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Save", on_click=lambda: self.save()).props(
                    "no-caps"
                ).set_enabled(not is_user_readonly())
                ui.button("Close", on_click=lambda: dialog.submit("close")).props(
                    "no-caps"
                )

        return dialog
```

---

## Two-Column & Master-Detail Selector Dialog Pattern

For complex entities that reference a parent/related entity (such as Visits or Adverse Events selecting a Patient):

```python
# src/views/dialogs/visit_dialog.py
from nicegui import ui
from nicegui.elements.dialog import Dialog
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


def validate_type(value: str | None) -> str | None:
    if not value:
        return "Visit type is required"
    return None


class StudyVisitDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.dialog: Dialog = self._build_dialog()

    async def show(self) -> str | None:
        return await self.dialog

    async def save(self) -> None:
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")

    def _build_dialog(self) -> Dialog:
        with ui.dialog() as dialog, ui.card().classes("w-240"):
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("Study Visit Details").classes("text-base font-semibold")

            with ui.row().classes("w-full gap-4"):
                # Left column: Related entity selector and summary details
                with ui.column().classes("flex-1"):
                    ui.select(
                        options=self.vm.get("patients"),
                        label="Patient",
                    ).bind_value(self.vm, "patient_id").on_value_change(
                        lambda: self.vm.call(
                            msg="load_patient", patient_id=self.vm.get("patient_id")
                        )
                    ).classes("w-full").props("dense")

                    selection = self.vm.get("selection")
                    ui.input(label="Patient Number").props("readonly dense").bind_value(
                        selection, "number"
                    ).classes("w-full")

                    ui.input(label="Start Date").props("readonly dense").bind_value(
                        selection, "start_date"
                    ).classes("w-full")

                    ui.input(label="Status").props("readonly dense").bind_value(
                        selection, "status_text"
                    ).classes("w-full")

                # Right column: Current entity editable fields
                with ui.column().classes("flex-1"):
                    ui.date_input(
                        label="Visit Date"
                    ).bind_value(self.vm, "visit_date").classes("w-full").props("dense")

                    ui.input(
                        label="Visit Type",
                        validation=validate_type,
                    ).bind_value(self.vm, "visit_type").classes("w-full").props("dense")

                    ui.textarea(
                        label="Comments"
                    ).bind_value(self.vm, "comments").classes("w-full").props("dense")

            # Validation error banner
            ui.markdown().classes("bg-orange-200 w-full p-2 rounded").bind_content_from(
                self.vm, "validation"
            ).bind_visibility_from(self.vm, "is_invalid")

            # Action buttons
            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Save", on_click=lambda: self.save()).props(
                    "no-caps"
                ).set_enabled(not is_user_readonly())
                ui.button("Close", on_click=lambda: dialog.submit("close")).props(
                    "no-caps"
                )

        return dialog
```

---

## Confirmation & Utility Dialogs (`DeleteWarningDialog`)

For non-ViewModel confirmations (e.g., deletion confirmation):

```python
# src/views/dialogs/delete_warning_dialog.py
from nicegui import ui
from nicegui.elements.dialog import Dialog


class DeleteWarningDialog:
    def __init__(self, message: str = "Are you sure you want to delete this record?"):
        with ui.dialog() as dialog, ui.card():
            with ui.row().classes("items-center gap-2"):
                ui.icon("warning", color="red", size="md")
                ui.label("Warning").classes("text-lg font-bold")
            with ui.row():
                ui.label(message)
            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Delete", on_click=lambda: dialog.submit("delete")).props(
                    "color=red no-caps"
                )
                ui.button("Cancel", on_click=lambda: dialog.submit("cancel")).props(
                    "no-caps"
                )
            self.dialog: Dialog = dialog

    async def show(self) -> str | None:
        return await self.dialog

    def close(self) -> None:
        self.dialog.close()
```

---

## Invoking Dialogs from Panels & Grids

### 1. New Record Creation (from Panel)
```python
# In EntityPanel:
async def _new_entity_dialog(self):
    entity_vm = EntityViewModel()
    user_name = app.storage.user.get("username", "Unknown")
    entity_vm.created_by = user_name
    entity_vm.updated_by = user_name
    entity_vm.created_at = datetime.now()
    entity_vm.updated_at = datetime.now()
    entity_vm.parent_id = self.parent_id

    dialog = EntityDialog(entity_vm)
    result = await dialog.show()
    if result == "save":
        # Refresh the parent list and broadcast updates
        await self.vm.call("load", parent_id=self.parent_id)
        await self.broadcast("entity_list", "load")
```

### 2. Editing an Existing Record (from AgGrid Row Edit Event)
```python
# In EntityGrid:
async def _edit_entity(self, row_data: dict) -> dict:
    vm = EntityViewModel()
    vm.from_dict(row_data)
    vm.updated_by = app.storage.user.get("username", "Unknown")
    vm.updated_at = datetime.now()

    dialog = EntityDialog(vm=vm)
    result = await dialog.show()
    if result == "save":
        await self.vm.call("load")
    return vm.to_dict()
```

### 3. Deletion Confirmation (from Panel)
```python
# In EntityPanel:
async def _on_delete_entity(self):
    if not is_user_readonly():
        dialog = DeleteWarningDialog("Are you sure you want to delete this entity?")
        result = await dialog.show()
        if result == "delete":
            selected_id = self.vm.get("selected_id")
            await self.vm.call("delete", entity_id=selected_id)
            await self.vm.call("load", parent_id=self.parent_id)
            await self.broadcast("entity_list", "load")
    else:
        ui.notification("You do not have permission to delete.", type="negative")
```

---

## Package Export Conventions

Export the dialog in `src/views/dialogs/__init__.py`:

```python
# src/views/dialogs/__init__.py
from .entity_dialog import EntityDialog as EntityDialog
from .delete_warning_dialog import DeleteWarningDialog as DeleteWarningDialog

__all__ = [
    "EntityDialog",
    "DeleteWarningDialog",
]
```

---

## Best Practices & Patterns

1. **Explicit Dialog Result**: Always submit explicit string tokens (`"save"`, `"close"`, `"cancel"`, `"delete"`) via `self.dialog.submit(...)`.
2. **Always Await Validation**: Inside `save()`, invoke `await self.vm.call("validate")` first and check `self.vm.get("is_invalid")` before proceeding to `self.vm.call("save")`.
3. **Readonly User Safeguard**: Disable the save button when `is_user_readonly()` is True using `.set_enabled(not is_user_readonly())`.
4. **Validation Banner**: Always include `ui.markdown().bind_content_from(self.vm, "validation").bind_visibility_from(self.vm, "is_invalid")` to render multi-line Markdown validation errors produced by the ViewModel.
5. **Dense Layout**: Use `.props("dense")` and `.classes("w-full")` on input controls to keep modal forms compact and visually aligned.
6. **Card Sizing**: Standardize modal widths using Tailwind classes (`w-120` for single column, `w-240` / `w-280` for two-column or master-detail layouts).

---

## Checklist

- [ ] Dialog class inherits from `View` and receives a single-entity `ViewModel`
- [ ] Uses `with ui.dialog() as dialog, ui.card():` to build UI
- [ ] All inputs two-way bound to `self.vm` via `.bind_value(self.vm, "field_name")`
- [ ] Field-level validators attached where required (`validation=validate_func`)
- [ ] Domain validation banner bound to `validation` and `is_invalid`
- [ ] `save()` calls `await self.vm.call("validate")` before `await self.vm.call("save")`
- [ ] `show()` returns `await self.dialog`
- [ ] Save button disabled for readonly users (`set_enabled(not is_user_readonly())`)
- [ ] Close / Cancel button calls `dialog.submit("close")` or `dialog.submit("cancel")`
- [ ] Dialog exported in `src/views/dialogs/__init__.py`
