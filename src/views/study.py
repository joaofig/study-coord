from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from models import Study
from viewmodels import StudyViewModel


class StudyEditor:
    def __init__(self):
        self.vm = StudyViewModel()

    async def save(self):
        await self.vm.save()

    def load(self, study: Study):
        self.vm.copy(study)

    def show(self):
        with ui.column():
            ui.label("Details").classes("text-h5 mt-4")
            ui.input(label="Name",
                     validation=validate_name
            ).classes("w-full").bind_value(self.vm, "name")
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

            with ui.row().classes("mt-4"):
                ui.button("Save", on_click=lambda: self.save()).props("icon=save").classes("ml-auto")
                ui.button("Delete", on_click=lambda: ui.notify("Study deleted")).props("icon=delete").classes("ml-2")


class StudyView:
    def __init__(self):
        self.editor = StudyEditor()

    def show(self):
        with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
            with splitter.before:
                self.study_grid_view()
            with splitter.after:
                self.editor.show()

    def study_grid_view(self):
        with ui.row().classes("w-full"):
            ui.label("Studies").classes("text-h4")
            ui.space()
            ui.button("Add Study", on_click=lambda: self.editor.load(Study.empty())).props("icon=add")
        with ui.row().classes("w-full h-full"):
            self.study_grid().classes("w-full h-full")

    def study_grid(self) -> AgGrid:
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
            'rowData': []
        }
        return ui.aggrid(grid_def)


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    return None


def save_study(vm: StudyViewModel) -> None:
    # Implement the logic to save the study details
    ui.notify(f"Study '{vm.name}' saved successfully!")



def study_editor(vm: StudyViewModel):
    # ui.label("Study Details").classes("text-h5")

    with ui.row():
        with ui.column():
            ui.label("Details").classes("text-h5 mt-4")
            ui.input(label="Name",
                     validation=validate_name
            ).classes("w-full").bind_value(vm, "name")
            ui.input(label="Sponsor").classes("w-full").bind_value(vm, "sponsor")

            with ui.row().classes("gap-2"):
                (ui.date_input(label="Start Date").bind_value(vm, "start_date"))
                (ui.date_input(label="End Date").bind_value(vm, "end_date"))

            with ui.row().classes("gap-2"):
                (ui.number(label="Protocol Visits", value=1)
                 .props('clearable')
                 .classes("w-full")
                 .bind_value(vm, "protocol_visits")
                 )
            with ui.row().classes("gap-2 w-full"):
                (ui.textarea(label="Description")
                 .classes("w-full")
                 .bind_value(vm, "description")
                 )

            with ui.row().classes("mt-4"):
                ui.button("Save", on_click=lambda: ui.notify("Study saved")).props("icon=save").classes("ml-auto")
                ui.button("Delete", on_click=lambda: ui.notify("Study deleted")).props("icon=delete").classes("ml-2")

        # with ui.column().classes("ml-8"):
        #     with ui.tabs() as tabs:
        #         visits = ui.tab(name="Visits", icon="event").classes("text-sky-600")
        #         monitoring = ui.tab(name="Monitoring", icon="monitor_heart").classes("text-sky-600")
        #         adverse_events = ui.tab(name="Events", icon="dangerous").classes("text-sky-600")
        #         patients = ui.tab(name="Patients", icon="personal_injury").classes("text-sky-600")
        #         researchers = ui.tab(name="Researchers", icon="group").classes("text-sky-600")
        #     with (
        #         ui.tab_panels(tabs, value=visits)
        #                 .props("vertical")
        #                 .classes("size-full")
        #     ):
        #         pass


def add_study():
    vm = StudyViewModel()


def study_grid() -> AgGrid:
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
        "rowData": []
    }
    return ui.aggrid(grid_def)


def study_grid_view():
    with ui.row().classes("w-full"):
        ui.label("Studies").classes("text-h4")
        ui.space()
        ui.button("Add Study", on_click=lambda: show_dialog()).props("icon=add")
    with ui.row().classes("w-full h-full"):
        study_grid().classes("w-full h-full")


def study_view():
    with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
        with splitter.before:
            study_grid_view()
        with splitter.after:
            study_editor()


