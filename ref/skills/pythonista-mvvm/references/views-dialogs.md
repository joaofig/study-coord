# Views and Dialogs

Views are the UI components built with NiceGUI. They are located in `src/views/`.

## Base View Class

All views must inherit from `View`. The `View` class automatically registers itself with the ViewModel for notifications.

```python
class MyView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        # build UI ...
```

## Grids (AgGrid)

Use AG Grid for displaying lists of data.

-   Bind the grid to an `ObservableList` in the ViewModel.
-   Use `on_change` of the `ObservableList` to call `grid.update()`.
-   Handle `selectionChanged` to notify the ViewModel.

### Edit Button in Grid

Use a custom `cellRenderer` to emit an event when an edit button is clicked.

```python
{
    "headerName": "Edit",
    "field": "id",
    ":cellRenderer": """
    (params) => {
        const btn = document.createElement('button');
        btn.innerText = '✏️';
        btn.addEventListener('click', () => {
            emitEvent('entity-row-edit', params.data);
        });
        return btn;
    }
    """
}
```

## Dialogs

Dialogs are used for creating and editing records.

-   Inherit from `View`.
-   Use `with ui.dialog() as dialog:` to create the dialog.
-   Return the `dialog` awaitable in an `async show()` method.
-   Call `dialog.submit(result)` to close the dialog and return a value.

```python
class EntityDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        with ui.dialog() as dialog, ui.card():
            ui.input("Name").bind_value(self.vm, "name")
            ui.button("Save", on_click=self.save)
            self.dialog = dialog

    async def show(self):
        return await self.dialog

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")
```

## Panels

Panels are container views that often host a Grid and action buttons.

-   Use `bind_enabled` to enable/disable buttons based on ViewModel state (e.g., `selected_id`).
-   Use `ui.tooltip` for button descriptions.

```python
class EntityPanel(View):
    def show(self):
        with ui.row():
            with ui.column():
                EntityGrid(self.vm).show()
            with ui.column():
                ui.button(icon="add", on_click=self._on_add)
                ui.button(icon="delete", on_click=self._on_delete) \
                    .bind_enabled(self.vm, "selected_id")
```
