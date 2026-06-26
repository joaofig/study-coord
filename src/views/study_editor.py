from nicegui import ui

from models import Study
from tools.messenger import MessengerHub
from viewmodels.patient import PatientViewModel
from viewmodels.view_model import ViewModel
from views.dialogs.study_patient import StudyPatientDialog
from views.patient_panel import PatientPanel
from views.study_researcher_grid import StudyResearcherGrid
from views.view import View


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    return None


class StudyEditor(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study = Study.empty()
        self.messenger = MessengerHub()["study"]
        self.messenger.subscribe("study_selected", self._study_selected)

    async def save(self):
        await self.command("save_study")

    async def _study_selected(self, **kwargs):
        study = kwargs.get("study")
        if study:
            study_id = study.get("id")
            if study_id:
                await self.command("load", study_id=study_id)

    async def load(self, study: Study):
        self.study = study
        await self.command("copy", study=study)

    def patient_panel(self):
        panel = PatientPanel()
        panel.show()

    def researcher_pane(self):
        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-1"):
                StudyResearcherGrid(self.vm).show()
            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add"):
                    ui.tooltip("Add Researcher")
                with ui.button(icon="delete"):
                    ui.tooltip("Delete Researcher")
                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")

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
                  on_change=lambda _: self.command("data_changed", property="name"))
             .classes("w-full")
             # .props("dense")
             .bind_value(self.vm, "name")
         )
        (ui.input(label="Sponsor", on_change=lambda _: self.command("data_changed", property="sponsor"))
             .classes("w-full")
             .bind_value(self.vm, "sponsor")
         )

        with ui.row().classes("gap-2"):
            (ui.date_input(label="Start Date", on_change=lambda _: self.command("data_changed", property="start_date"))
                .bind_value(self.vm, "start_date"))
            (ui.date_input(label="End Date", on_change=lambda _: self.command("data_changed", property="end_date"))
                .bind_value(self.vm, "end_date"))

        with ui.row().classes("gap-2"):
            (ui.number(label="Protocol Visits", value=1, on_change=lambda _: self.command("data_changed", property="proto_visits"))
                 .props('clearable')
                 .classes("w-full")
                 .bind_value(self.vm, "visits", strict=True)
             )
        with ui.row().classes("gap-2 w-full"):
            (ui.textarea(label="Comments",
                         on_change=lambda _: self.command("data_changed", property="comments"))
                 .classes("w-full")
                 .bind_value(self.vm, "comments")
             )

    async def show_patient_dialog(self):
        patient_vm = PatientViewModel()
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()

        if result == "save":
            # Reload the patient's grid after saving the patient
            await self.vm.message("load_patients")

    def details_pane(self):
        with ui.tabs().props("horizontal").classes("p-0").bind_visibility(self.vm, "is_old") as tabs:
            # visits = ui.tab("Visits", icon="event").classes("text-sky-800")
            # monitoring = ui.tab("Monitoring", icon="monitor_heart").classes("text-sky-800")
            # adverse_events = ui.tab("Events", icon="dangerous").classes("text-sky-800")
            patients = ui.tab("Patients", icon="personal_injury").classes("text-sky-800")
            researchers = ui.tab("Researchers", icon="group").classes("text-sky-800")
        with (ui.tab_panels(tabs, value=patients)
                .classes("size-full")):
            with (ui.tab_panel(patients)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.patient_panel()

            with (ui.tab_panel(researchers)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.researcher_pane()

    def show(self):
        with ui.splitter(value=35).classes("w-full") as splitter:
            with splitter.before:
                self.study_pane()
            with splitter.after:
                self.details_pane()
