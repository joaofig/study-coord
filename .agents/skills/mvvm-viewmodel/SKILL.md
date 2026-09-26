---
name: mvvm-viewmodel
description: Use when creating or modifying single or plural (list) ViewModels in NiceGUI MVVM architecture given a DTO. Triggers on "mvvm-viewmodel", "ViewModel", "bindable_dataclass", "single mvvm-viewmodel", "list mvvm-viewmodel", "GridList", "ObservableList", "MVVM state", "MVVM mvvm-viewmodel".
writes-artifact: false
---

# ViewModel Pattern (Single & List ViewModels)

This skill provides comprehensive instructions, patterns, and guidelines for implementing ViewModels in this NiceGUI MVVM project, deriving reactive UI controllers directly from a generic DTO (Data Transfer Object).

## Core Architecture & Principles

ViewModels manage the presentation state and handle user actions in `app/src/viewmodels/`. They coordinate between the Views (NiceGUI components) and Models (domain services).

- **Base Class**: All ViewModels inherit from `ViewModel` (`nicemvvm.viewmodels.view_model.ViewModel`).
- **Separation of Concerns**: ViewModels never create UI elements (buttons, inputs, grids) directly. Views bind to ViewModel state.
- **Messenger Bus**: Decoupled cross-component communication using `self.broadcast(channel, message, **kwargs)` and `self.subscribe(channel, message, handler)`.
- **Command Dispatcher**: Actions and invocations from Views are routed through `_on_call(self, msg: str, **kwargs) -> Any`.

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
```

---

## Single vs Plural (List) ViewModels Comparison

| Dimension | Single Entity ViewModel (`<Entity>ViewModel`) | Plural / List ViewModel (`<Entity>ListViewModel`) |
| :--- | :--- | :--- |
| **Primary Purpose** | Form editing, detail panels, input validation, tracking dirty state for a single record. | Collection display, AgGrid tables, selection tracking, search/filtering, multi-item deletion. |
| **Class Decorator** | `@binding.bindable_dataclass` | Standard class (No `@bindable_dataclass` on list VM) |
| **Initialization** | `__post_init__(self)` calling `super().__init__()` | `__init__(self)` calling `super().__init__()` |
| **Data Container** | Individual bindable primitive attributes (`int`, `str`, `date`) | `GridList()` or `ObservableList()` containing list of dicts |
| **Messaging Role** | Broadcasts `"saved"`, `"updated"` events | Subscribes to `"saved"`, `"deleted"`, parent `"selected"` events; broadcasts `"selected"`, `"deleted"` |
| **Model Invocations** | `model.load(id)`, `model.save(dto)`, `model.code_exists(code)` | `model.list(parent_id)`, `model.delete(id)` |

---

## 1. Single Entity ViewModel Pattern (`<Entity>ViewModel`)

Used for creating, editing, validating, and saving a single record in dialogs or detail panels.

### Key Characteristics
1. Decorated with `@binding.bindable_dataclass` from `nicegui`.
2. Defines primitive attributes matching the DTO fields (using ISO format strings for dates bound to `ui.input`).
3. Tracks validation feedback in `self.validation` (Markdown formatted string) and `self.is_invalid: bool`.
4. Tracks dirty / modification state using `self.changed: bool` and/or `self.change_set = ObservableSet()`.
5. Provides DTO conversions (`to_dto`, `copy` / `from_dict`, `to_dict`).

### Blueprint: `<Entity>ViewModel`

Create at `app/src/viewmodels/<module>/<entity>.py`:

```python
# src/viewmodels/study/entity.py
from datetime import date, datetime
from typing import Any

from nicegui import binding
from src.dtos.entity import EntityDTO
from src.models.entity import EntityModel
from nicemvvm.tools.user import dict_to_datetime
from nicemvvm.tools.validation import is_date
from nicemvvm.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class EntityViewModel(ViewModel):
    entity_id: int = 0
    parent_id: int = 0
    code: str = ""
    name: str = ""
    status: str = "active"
    start_date: str = date.today().isoformat()
    end_date: str | None = None
    comments: str = ""

    # Audit fields
    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    # State & Validation
    is_invalid: bool = False
    validation: str = ""
    changed: bool = False
    is_old: bool = False

    model = EntityModel()

    def __post_init__(self):
        super().__init__()

    def copy(self, entity: EntityDTO):
        """Populate the ViewModel fields from a DTO."""
        self.entity_id = entity.entity_id or 0
        self.parent_id = entity.parent_id or 0
        self.code = entity.code
        self.name = entity.name
        self.status = entity.status
        self.start_date = entity.start_date.isoformat() if entity.start_date else date.today().isoformat()
        self.end_date = entity.end_date.isoformat() if entity.end_date else None
        self.comments = entity.comments or ""

        self.created_at = entity.created_at
        self.created_by = entity.created_by
        self.updated_at = entity.updated_at
        self.updated_by = entity.updated_by

        self.changed = False
        self.is_old = self.entity_id > 0
        self.validation = ""
        self.is_invalid = False

    def from_dict(self, data: dict):
        """Populate the ViewModel fields from a dictionary."""
        self.entity_id = data.get("entity_id", 0) or 0
        self.parent_id = data.get("parent_id", 0) or 0
        self.code = data.get("code", "")
        self.name = data.get("name", "")
        self.status = data.get("status", "active")
        self.start_date = data.get("start_date", date.today().isoformat())
        self.end_date = data.get("end_date")
        self.comments = data.get("comments", "") or ""

        self.created_at = dict_to_datetime(data, "created_at") or datetime.now()
        self.created_by = data.get("created_by", "")
        self.updated_at = dict_to_datetime(data, "updated_at") or datetime.now()
        self.updated_by = data.get("updated_by", "")

        self.changed = False
        self.is_old = self.entity_id > 0

    def to_dto(self) -> EntityDTO:
        """Convert current ViewModel state to a typed DTO."""
        return EntityDTO(
            entity_id=self.entity_id,
            parent_id=self.parent_id,
            code=self.code,
            name=self.name,
            status=self.status,
            start_date=date.fromisoformat(self.start_date) if self.start_date else date.today(),
            end_date=date.fromisoformat(self.end_date) if self.end_date else None,
            comments=self.comments or "",
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    def to_dict(self) -> dict:
        """Serialize current state to dictionary."""
        return {
            "entity_id": self.entity_id,
            "parent_id": self.parent_id,
            "code": self.code,
            "name": self.name,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "comments": self.comments or "",
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by,
        }

    async def save(self) -> bool:
        """Validate, persist to mvvm-model, log changes, and broadcast save event."""
        if not await self.validate():
            return False

        entity = self.to_dto()
        entity.log_change(self.entity_id)
        await self.model.save(entity)
        if entity.entity_id:
            self.entity_id = entity.entity_id

        self.changed = False
        self.is_old = True
        await self.broadcast(
            channel="entity",
            message="saved",
            entity_id=self.entity_id,
            parent_id=self.parent_id,
        )
        return True

    async def validate(self) -> bool:
        """Execute business and formatting validations."""
        self.validation = ""
        self.is_invalid = False

        if not self.code or len(self.code.strip()) == 0:
            self.validation += "**Code** is required.  \r\n"
        elif self.entity_id == 0 and await self.model.code_exists(self.code, self.parent_id):
            self.validation += "**Code** already exists.  \r\n"

        if not self.name or len(self.name.strip()) == 0:
            self.validation += "**Name** is required.  \r\n"
        elif len(self.name) < 3:
            self.validation += "**Name** must be at least 3 characters.  \r\n"
        elif len(self.name) > 128:
            self.validation += "**Name** must be at most 128 characters.  \r\n"

        if self.start_date and not is_date(self.start_date):
            self.validation += "**Start date** must be a valid date.  \r\n"

        if self.end_date and not is_date(self.end_date):
            self.validation += "**End date** must be a valid date.  \r\n"

        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.validation += "**End date** must be after **Start date**.  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "save":
                return await self.save()
            case "validate":
                return await self.validate()
            case "load":
                entity_id = kwargs.get("entity_id", 0)
                if entity_id:
                    entity = await self.model.load(int(entity_id))
                    if entity:
                        self.copy(entity)
            case "copy":
                dto = kwargs.get("dto")
                if dto:
                    self.copy(dto)
        return None
```

---

## 2. Plural / List ViewModel Pattern (`<Entity>ListViewModel`)

Used for managing collections of records, backing AgGrid or table views, handling selection, filtering, and cross-component messaging.

### Key Characteristics
1. Standard Python class inheriting from `ViewModel` (do **not** decorate with `@binding.bindable_dataclass`).
2. Holds items in an observable collection: `items = GridList()` (from `nicemvvm.tools.observability`).
3. Tracks `selected_id: int = 0` and optional scoping parent foreign key (e.g. `parent_id: int = 0`).
4. Subscribes in `__init__` to entity change events (`"saved"`, `"deleted"`) and parent context changes (`"selected"`).
5. Provides command dispatcher `_on_call` for `"load"`, `"select"`, `"delete"`.

### Blueprint: `<Entity>ListViewModel`

Create at `app/src/viewmodels/<module>/<entity>_list.py`:

```python
# src/viewmodels/study/entity_list.py
from typing import Any

from src.models.entity import EntityModel
from nicemvvm.tools.observability import GridList
from nicemvvm.viewmodels.view_model import ViewModel


class EntityListViewModel(ViewModel):
    entities = GridList()
    parent_id: int = 0
    selected_id: int = 0
    model: EntityModel = EntityModel()

    def __init__(self):
        super().__init__()
        # Subscribe to parent selection to update context
        self.subscribe(
            channel="parent",
            message="selected",
            handler=self._handle_parent_selected,
        )
        # Subscribe to entity save events to reload grid
        self.subscribe(
            channel="entity",
            message="saved",
            handler=self._handle_saved,
        )

    async def _load_entities(self, parent_id: int = 0):
        """Fetch records from Model and replace GridList contents."""
        entities = await self.model.list(parent_id)
        self.entities.replace([e.to_dict() for e in entities])

    async def _handle_parent_selected(self, **kwargs):
        parent_id = kwargs.get("parent_id", 0)
        if parent_id:
            self.parent_id = parent_id
            await self._load_entities(self.parent_id)
        else:
            self.parent_id = 0
            self.selected_id = 0
            self.entities.clear()
        self.selected_id = 0

    async def _handle_saved(self, **kwargs):
        await self._load_entities(self.parent_id)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                parent_id = kwargs.get("parent_id", self.parent_id)
                self.parent_id = int(parent_id)
                await self._load_entities(self.parent_id)

            case "select":
                entity_id = kwargs.get("entity_id", 0)
                if entity_id:
                    self.selected_id = int(entity_id)
                    await self.broadcast(
                        channel="entity",
                        message="selected",
                        entity_id=self.selected_id,
                        parent_id=self.parent_id,
                    )

            case "delete":
                entity_id = kwargs.get("entity_id", 0)
                if entity_id:
                    entity_id = int(entity_id)
                    await self.model.delete(entity_id)
                    self.entities.delete("entity_id", entity_id)
                    if self.selected_id == entity_id:
                        self.selected_id = 0
                    await self.broadcast(
                        channel="entity",
                        message="deleted",
                        entity_id=entity_id,
                        parent_id=self.parent_id,
                    )
        return None
```

---

## Package Export Conventions

Always export both ViewModels in `src/viewmodels/__init__.py`:

```python
# src/viewmodels/__init__.py
from src.viewmodels.study.entity import EntityViewModel
from src.viewmodels.study.entity_list import EntityListViewModel

__all__ = [
    # ...
    "EntityViewModel",
    "EntityListViewModel",
]
```

---

## Best Practices & Patterns

1. **Keep UI Construction Out**: ViewModels should never instantiate UI elements (like `ui.button` or `ui.label`). Keep ViewModels pure state and command managers.
2. **Observability Choices**:
   - For single entity form binding: Use `@binding.bindable_dataclass`.
   - For lists/grids: Use `GridList()` which wraps `ObservableList` and supports operations like `.replace()`, `.delete(field, val)`.
3. **Date Format Consistency**: NiceGUI date inputs bind cleanly with ISO 8601 strings (`YYYY-MM-DD`). In Single ViewModels, store dates as ISO strings and convert to `date` objects in `to_dto()`.
4. **Messenger Channels & Message Names**:
   - Channel: noun identifying the entity (e.g. `"patient"`, `"study"`, `"researcher"`).
   - Standard Messages: `"saved"`, `"deleted"`, `"selected"`, `"load"`.
5. **Always Call `super().__init__()`**: In single ViewModels, call in `__post_init__`; in list ViewModels, call in `__init__`.

---

## Checklists

### Single ViewModel Checklist
- [ ] Decorated with `@binding.bindable_dataclass`
- [ ] Inherits from `ViewModel`
- [ ] `__post_init__` calls `super().__init__()`
- [ ] Contains all fields from DTO with default values
- [ ] Implements `copy(dto)`, `from_dict(dict)`, `to_dto()`, and `to_dict()`
- [ ] Implements async `validate()` setting `is_invalid` and markdown `validation`
- [ ] Implements async `save()` calling `dto.log_change(id)`, `model.save(dto)`, and broadcasting `"saved"`
- [ ] Implements `_on_call` for `"save"`, `"validate"`, and `"load"`

### List ViewModel Checklist
- [ ] Standard class (not `@bindable_dataclass`) inheriting from `ViewModel`
- [ ] `__init__` calls `super().__init__()` and registers `subscribe` handlers
- [ ] Holds collection in `GridList()`
- [ ] Manages `selected_id` and optional `parent_id`
- [ ] Implements `_on_call` handling `"load"`, `"select"`, and `"delete"`
- [ ] On selection/deletion, updates collection and broadcasts corresponding events
- [ ] Both ViewModels exported in `src/viewmodels/__init__.py`
