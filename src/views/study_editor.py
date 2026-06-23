from nicegui import ui

from models import Study
from viewmodels import StudyViewModel
from viewmodels.patient import PatientViewModel
from views.dialogs.study_patient import StudyPatientDialog
from views.study_patient_grid import StudyPatientGrid


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

    async def show_patient_dialog(self):
        patient_vm = PatientViewModel()
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()

        if result == "save":
            ui.notify("Patient saved")

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
                        with ui.button(icon="add", on_click=lambda: self.show_patient_dialog()):
                            ui.tooltip("Add Patient")
                        with ui.button(icon="delete"):
                            ui.tooltip("Delete Patient")
                        with ui.button(icon="table_view"):
                            ui.tooltip("Export to Excel")

            with ui.tab_panel(researchers).bind_visibility(self.vm, "is_old"):
                ui.label("Researchers").classes("text-h4")
                ui.label("Content of researchers")

    def show(self):
        with ui.splitter(value=35).classes("w-full") as splitter:
            with splitter.before:
                self.study_pane()
            with splitter.after:
                self.details_pane()
