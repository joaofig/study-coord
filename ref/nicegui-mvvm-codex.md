I’ll use the `nicegui-mvvm` skill since this is specifically about structuring a NiceGUI app around MVVM and data binding.

Use MVVM as a discipline, not as a framework layer NiceGUI owns. The clean rule is:

- **Models**: plain domain/data objects, no NiceGUI imports.
- **Database layer**: repositories/unit-of-work under `src/db`, no NiceGUI imports.
- **ViewModels**: page/application state and commands, no direct UI construction.
- **Views**: NiceGUI elements, bindings, refreshable regions, dialogs, notifications.

NiceGUI fits this well because UI logic is Python-side, supports data binding, and has `@ui.refreshable`/`@ui.refreshable_method` for rebuilding only selected UI sections. NiceGUI bindings work against ordinary Python objects, and refreshable functions are the intended way to rebuild a subtree without recreating the whole page. ([raw.githubusercontent.com](https://raw.githubusercontent.com/zauberzeug/nicegui/main/nicegui/llms.md))

**Suggested Structure**
```text
src/
  main.py

  models/
    study.py
    participant.py

  db/
    connection.py
    schema.py
    repositories/
      study_repository.py
      participant_repository.py
    unit_of_work.py

  viewmodels/
    study_list_vm.py
    study_editor_vm.py
    dialog_vm.py

  views/
    pages/
      studies_page.py
    components/
      study_master_list.py
      study_detail_panel.py
      study_editor_dialog.py
    dialogs/
      confirm_dialog.py
      study_dialog.py

tests/
  db/
  viewmodels/
  views/
```

**Database Layer**
Keep SQLite access behind repositories:

```python
# src/db/repositories/study_repository.py
from src.models.study import Study

class StudyRepository:
    def __init__(self, db):
        self.db = db

    async def list(self) -> list[Study]:
        ...

    async def get(self, study_id: int) -> Study | None:
        ...

    async def save(self, study: Study) -> Study:
        ...

    async def delete(self, study_id: int) -> None:
        ...
```

The ViewModel depends on repositories, not SQLite details:

```python
# src/viewmodels/study_list_vm.py
from dataclasses import dataclass, field
from src.models.study import Study
from src.db.repositories.study_repository import StudyRepository

@dataclass
class StudyListViewModel:
    studies: list[Study] = field(default_factory=list)
    selected_id: int | None = None
    loading: bool = False
    error: str | None = None

    def __init__(self, repository: StudyRepository):
        self.repository = repository
        self.studies = []
        self.selected_id = None
        self.loading = False
        self.error = None

    async def load(self) -> None:
        self.loading = True
        self.error = None
        try:
            self.studies = await self.repository.list()
        except Exception as exc:
            self.error = str(exc)
        finally:
            self.loading = False

    async def delete_selected(self) -> None:
        if self.selected_id is None:
            return
        await self.repository.delete(self.selected_id)
        self.selected_id = None
        await self.load()
```

Avoid long blocking database work in NiceGUI callbacks. NiceGUI runs UI callbacks on a shared async event loop, so blocking I/O can freeze the application for all users. Use async DB access where possible, or move synchronous SQLite operations through `asyncio.to_thread`. ([raw.githubusercontent.com](https://raw.githubusercontent.com/zauberzeug/nicegui/main/nicegui/llms.md))

**Views And Binding**
Views should create elements and bind them to ViewModel properties:

```python
# src/views/pages/studies_page.py
from nicegui import ui, background_tasks
from src.viewmodels.study_list_vm import StudyListViewModel
from src.views.components.study_master_list import StudyMasterList
from src.views.components.study_detail_panel import StudyDetailPanel

class StudiesPage:
    def __init__(self, vm: StudyListViewModel):
        self.vm = vm

    def render(self) -> None:
        with ui.row().classes('w-full h-full'):
            self.master = StudyMasterList(self.vm)
            self.master.render()

            self.detail = StudyDetailPanel(self.vm)
            self.detail.render()

        background_tasks.create(self._load())

    async def _load(self) -> None:
        await self.vm.load()
        self.master.refresh()
```

Prefer page-local ViewModel instances. NiceGUI module-level state is shared across users, while each `@ui.page` call creates a fresh scope per visitor/page load. ([raw.githubusercontent.com](https://raw.githubusercontent.com/zauberzeug/nicegui/main/nicegui/llms.md))

```python
# src/main.py
from nicegui import ui
from src.db.connection import create_db
from src.db.repositories.study_repository import StudyRepository
from src.viewmodels.study_list_vm import StudyListViewModel
from src.views.pages.studies_page import StudiesPage

@ui.page('/studies')
def studies_page():
    db = create_db()
    vm = StudyListViewModel(StudyRepository(db))
    StudiesPage(vm).render()

ui.run()
```

**Master List Updates**
For master lists, use a refreshable component. Do not rebuild the whole page after every create/edit/delete.

```python
# src/views/components/study_master_list.py
from nicegui import ui

class StudyMasterList:
    def __init__(self, vm):
        self.vm = vm

    @ui.refreshable_method
    def render(self):
        with ui.column().classes('w-80 gap-1'):
            ui.label('Studies').classes('text-lg font-medium')

            if self.vm.loading:
                ui.spinner()
                return

            if self.vm.error:
                ui.label(self.vm.error).classes('text-negative')
                return

            for study in self.vm.studies:
                selected = study.id == self.vm.selected_id
                ui.button(
                    study.title,
                    on_click=lambda s=study: self.select(s.id),
                    color='primary' if selected else None,
                ).classes('w-full justify-start')

    def select(self, study_id: int) -> None:
        self.vm.selected_id = study_id
        self.render.refresh()

    def refresh(self) -> None:
        self.render.refresh()
```

Use `@ui.refreshable_method` for repeated or list-shaped UI. Use direct binding for scalar fields like selected title, error text, visibility, or form values. NiceGUI bindings automatically propagate changes, so simple field updates usually do not need manual `.update()`. ([raw.githubusercontent.com](https://raw.githubusercontent.com/zauberzeug/nicegui/main/nicegui/llms.md))

**Dialog Interactions**
Keep dialog UI in `views/dialogs`, but keep dialog state in a small ViewModel.

```python
# src/viewmodels/study_editor_vm.py
from dataclasses import dataclass

@dataclass
class StudyEditorViewModel:
    id: int | None = None
    title: str = ''
    description: str = ''

    def load_from(self, study) -> None:
        self.id = study.id
        self.title = study.title
        self.description = study.description

    def to_command(self):
        return {
            'id': self.id,
            'title': self.title.strip(),
            'description': self.description.strip(),
        }
```

```python
# src/views/dialogs/study_dialog.py
from nicegui import ui

class StudyDialog:
    def __init__(self, vm):
        self.vm = vm
        self.result = None

        with ui.dialog() as self.dialog, ui.card().classes('w-96'):
            ui.input('Title').bind_value(self.vm, 'title').classes('w-full')
            ui.textarea('Description').bind_value(self.vm, 'description').classes('w-full')

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.cancel)
                ui.button('Save', on_click=self.save, color='primary')

    async def open(self):
        self.result = None
        self.dialog.open()
        await self.dialog
        return self.result

    def save(self):
        self.result = self.vm.to_command()
        self.dialog.close()

    def cancel(self):
        self.result = None
        self.dialog.close()
```

Then the page/component orchestrates the interaction:

```python
async def edit_study(self, study):
    editor_vm = StudyEditorViewModel()
    editor_vm.load_from(study)

    dialog = StudyDialog(editor_vm)
    command = await dialog.open()

    if command is None:
        return

    await self.vm.save(command)
    self.render.refresh()
```

That keeps the ViewModel testable: tests can call `load`, `save`, `delete_selected`, and validation logic without importing NiceGUI. The View remains thin: build elements, bind fields, call ViewModel commands, refresh only the affected section.

The main pattern I would use is: **repositories mutate durable state, ViewModels mutate page state, Views bind and refresh.** That gives you a NiceGUI app that feels native to NiceGUI while still keeping MVVM boundaries clean.