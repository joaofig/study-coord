# ViewModels

ViewModels manage the state of the UI and coordinate between Models and Views. They are located in `src/viewmodels/`.

## Structure

-   Inherit from the `ViewModel` base class.
-   Use `@binding.bindable_dataclass` for reactive properties.
-   Override `__post_init__` and call `super().__init__()`.
-   Implement `_on_call(msg, **kwargs)` to handle messages.

### Single Entity ViewModel

Used for forms and editing a single record.

```python
@binding.bindable_dataclass
class EntityViewModel(ViewModel):
    entity_id: int = 0
    name: str = ""
    changed: bool = False

    def __post_init__(self):
        super().__init__()

    async def save(self):
        entity = Entity(id=self.entity_id, name=self.name)
        await entity.save()
        self.entity_id = entity.id
        self.changed = False
        await self.broadcast("entity", "saved")

    async def _on_call(self, msg: str, **kwargs):
        match msg:
            case "save":
                await self.save()
            case "load":
                # ... load logic ...
```

### List ViewModel

Used for grids and managing collections.

-   Use `ObservableList` for the data source.
-   Subscribe to relevant messages (e.g., `saved`, `study_selected`).

```python
class EntityListViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.entities = ObservableList()
        self.subscribe(channel="entity", message="saved", handler=self._handle_saved)

    async def _load(self, parent_id: int):
        model = EntityList()
        self.entities.clear()
        items = await model.load_from_parent(parent_id)
        self.entities.extend([i.to_dict() for i in items])
```

## Data Access in Views

Views should use the `get()` method to access non-bindable properties from the ViewModel.

```python
# In View
self.select = ui.select(options=self.vm.get("patients"), label="Patient")
```

## Messaging (Messenger)

-   **Broadcast**: `await self.broadcast(channel, message, **kwargs)`
-   **Subscribe**: `self.subscribe(channel, message, handler)`

Common channels: `study`, `patient`, `visit`, `event`.
Common messages: `saved`, `selected`, `deleted`, `load`.
