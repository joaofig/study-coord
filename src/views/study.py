from typing import Mapping, Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from models import Study
from viewmodels import StudyViewModel
from viewmodels.study import StudyListViewModel


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    return None


class StudyEditor:
    def __init__(self):
        self.vm = StudyViewModel()
        self.study = Study.empty()

    async def save(self):
        await self.vm.async_message("save")

    def load(self, study: Study):
        self.study = study
        self.vm.copy(study)

    def show(self):
        with ui.column():
            with ui.row().classes("mt-2 w-full"):
                (ui.button("Save", on_click=lambda: self.save())
                    .props("icon=save")
                    .classes("text-xs")
                )
                (ui.button("Undo", on_click=lambda: self.load(self.study))
                    .props("icon=undo")
                    .classes("text-xs")
                )
                ui.space()
                (ui.button("Delete", on_click=lambda: ui.notify("Study deleted"))
                    .classes("text-xs")
                    .props("icon=delete")
                    .props("color=red")
                )

            (ui.input(label="Name", validation=validate_name)
                .classes("w-full")
                .bind_value(self.vm, "name")
            )
            (ui.input(label="Sponsor")
                 .classes("w-full")
                 .bind_value(self.vm, "sponsor")
            )

            with ui.row().classes("gap-2"):
                (ui.date_input(label="Start Date").bind_value(self.vm, "start_date"))
                (ui.date_input(label="End Date").bind_value(self.vm, "end_date"))

            with ui.row().classes("gap-2"):
                (ui.number(label="Protocol Visits", value=1)
                 .props('clearable')
                 .classes("w-full")
                 .bind_value(self.vm, "visits")
                 )
            with ui.row().classes("gap-2 w-full"):
                (ui.textarea(label="Comments")
                 .classes("w-full")
                 .bind_value(self.vm, "comments")
                 )



class StudyGrid:
    def __init__(self, vm: StudyListViewModel) -> None:
        self.vm = vm
        self.grid: Any = None
        vm.register(self._vm_notification)

    def _vm_notification(self, action: str, data: Any = None) -> None:
        if action == "list_changed":
            self.grid.options["rowData"] = [row.do_dict() for row in self.vm.studies]
            self.grid.update()

    def show(self) -> AgGrid:
        columns = [
            {"headerName": "ID", "field": "id", "hide": True},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Sponsor", "field": "sponsor", "sortable": True, "align": "left"},
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left"},
            {"headerName": "End", "field": "end_date", "sortable": True, "align": "left"},
            {"headerName": "Patients", "field": "patients", "sortable": True, "align": "right"},
            {"headerName": "Visits", "field": "visits", "sortable": True, "align": "right"},
            {"headerName": "Researchers", "field": "researchers", "sortable": True, "align": "right"},
            {"headerName": "Events", "field": "adverse_events", "sortable": True, "align": "right"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            ":getRowId": "(params) => String(params.data.id)"
        }
        self.grid = ui.aggrid(grid_def).classes("w-full h-full")
        return self.grid


class StudyView:
    def __init__(self, view_model: StudyListViewModel):
        self.editor = StudyEditor()
        self.vm = view_model
        self.grid = StudyGrid(self.vm)

    async def load(self):
        await self.vm.load()

    def show(self):
        with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
            with splitter.before:
                self.grid.show()
            with splitter.after:
                self.editor.show()
