from typing import Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from src.models import Study
from src.viewmodels import StudyViewModel
from src.viewmodels.study import StudyListViewModel
from viewmodels.view_model import ViewModel


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    return None


class StudyEditor:
    def __init__(self, vm: StudyViewModel):
        self.vm = vm
        self.study = Study.empty()

    async def save(self):
        await self.vm.async_message("save_study")

    def load(self, study: Study):
        self.study = study
        self.vm.copy(study)

    def study_pane(self):
        with ui.row().classes("mt-2 w-full"):
            (ui.button("New", on_click=lambda: self.load(Study.empty()))
             .props("icon=add")
             .classes("text-xs")
             )
            (ui.button("Save", on_click=lambda: self.save())
                .props("icon=save")
                .classes("text-xs")
                .disable()
                .bind_enabled(self.vm, "changed")
             )
            (ui.button("Undo", on_click=lambda: self.load(self.study))
             .props("icon=undo")
             .classes("text-xs")
             )
            ui.space()
            (ui.button("Delete", on_click=lambda: ui.notify("Study deleted"))
                .classes("text-xs mr-2")
                .props("icon=delete")
                .props("color=red")
                .disable()
             )

        (ui.input(label="Name", validation=validate_name, 
                  on_change=lambda _: self.vm.async_message("data_changed", "name"))
             .classes("w-full")
             # .props("dense")
             .bind_value(self.vm, "name")
         )
        (ui.input(label="Sponsor", on_change=lambda _: self.vm.async_message("data_changed", "sponsor"))
             .classes("w-full")
             .bind_value(self.vm, "sponsor")
         )

        with ui.row().classes("gap-2"):
            (ui.date_input(label="Start Date", on_change=lambda _: self.vm.async_message("data_changed", "start_date"))
                .bind_value(self.vm, "start_date"))
            (ui.date_input(label="End Date", on_change=lambda _: self.vm.async_message("data_changed", "end_date"))
                .bind_value(self.vm, "end_date"))

        with ui.row().classes("gap-2"):
            (ui.number(label="Protocol Visits", value=1, on_change=lambda _: self.vm.async_message("data_changed", "proto_visits"))
                 .props('clearable')
                 .classes("w-full")
                 .bind_value(self.vm, "visits", strict=True)
             )
        with ui.row().classes("gap-2 w-full"):
            (ui.textarea(label="Comments", 
                         on_change=lambda _: self.vm.async_message("data_changed", "comments"))
                 .classes("w-full")
                 .bind_value(self.vm, "comments")
             )

    def details_pane(self):
        with ui.tabs().props("horizontal").classes("p-0").bind_visibility(self.vm, "is_old") as tabs:
            # visits = ui.tab("Visits", icon="event").classes("text-sky-800")
            # monitoring = ui.tab("Monitoring", icon="monitor_heart").classes("text-sky-800")
            # adverse_events = ui.tab("Events", icon="dangerous").classes("text-sky-800")
            patients = ui.tab("Patients", icon="personal_injury").classes("text-sky-800")
            researchers = ui.tab("Researchers", icon="group").classes("text-sky-800")
        with (ui.tab_panels(tabs, value=patients)
                .classes("size-full")):
            # with ui.tab_panel(visits):
            #     ui.label("Visits").classes("text-h4")
            #     ui.label("Content of visits")
            #
            # with ui.tab_panel(monitoring):
            #     ui.label("Monitoring").classes("text-h4")
            #     ui.label("Content of monitoring")
            #
            # with ui.tab_panel(adverse_events):
            #     ui.label("Adverse Events").classes("text-h4")
            #     ui.label("Content of adverse events")

            with (ui.tab_panel(patients)
                    .classes("pl-2 pt-0 pb-0 pr-0").bind_visibility(self.vm, "is_old")):
                with ui.row().classes("w-full h-full"):

                    with ui.column().classes("h-full flex-1"):
                        StudyPatientGrid(self.vm).show()
                    with ui.column().classes("h-full flex-none"):
                        ui.button(icon="add")
                        ui.button(icon="delete")

            with ui.tab_panel(researchers).bind_visibility(self.vm, "is_old"):
                ui.label("Researchers").classes("text-h4")
                ui.label("Content of researchers")

    def show(self):
        with ui.splitter(value=35).classes("w-full") as splitter:
            with splitter.before:
                self.study_pane()
            with splitter.after:
                self.details_pane()


class StudyPatientGrid:
    def __init__(self, vm: ViewModel):
        self.vm = vm
        self.grid: Any = None

    def show(self) -> AgGrid:
        columns = [
            {"headerName": "ID", "field": "id", "hide": True},
            {"headerName": "Number", "field": "number", "sortable": True, "align": "left"},
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left"},
            {"headerName": "End", "field": "end_date", "sortable": True, "align": "left"},
            {"headerName": "Status", "field": "status", "sortable": True, "align": "left"},
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


class StudyGrid:
    def __init__(self, vm: StudyListViewModel) -> None:
        self.vm = vm
        self.grid: Any = None
        vm.register(self._vm_notification)

    def _vm_notification(self, action: str, data: Any = None) -> None:
        if action == "list_changed":
            self.grid.options["rowData"] = self.vm.studies
            self.grid.update()

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            # ui.notify(f"{row}")
            await self.vm.async_message("study_selected", row)
        else:
            # ui.notify('No row selected!')
            await self.vm.async_message("study_unselected", row)

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
            "rowSelection": {"mode": "singleRow"},
            ":getRowId": "(params) => String(params.data.id)"
        }
        self.grid = ui.aggrid(grid_def).classes("w-full h-full")
        # self.grid.on("rowClicked",
        #              self._row_selected, # ui.notify(event.args["data"]),
        #              ["data"]
        #             )
        self.grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return self.grid

    async def _row_selected(self, event):
        row_data = event.args["data"]
        await self.vm.async_message("study_selected", row_data)


class StudyView:
    def __init__(self, view_model: StudyListViewModel):
        self.editor = StudyEditor(view_model.study_vm)
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
