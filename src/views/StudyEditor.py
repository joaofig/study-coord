from nicegui import ui

from models import Study
from src.viewmodels import PatientListViewModel, MonitoringListViewModel
from src.viewmodels import PatientViewModel
from src.viewmodels.ViewModel import ViewModel
from src.views.dialogs.StudyPatientDialog import StudyPatientDialog
from src.views.StudyMonitoringPanel import StudyMonitoringPanel
from src.views.StudyPatientPanel import StudyPatientPanel
from src.views.StudyResearcherGrid import StudyResearcherGrid
from src.views.View import View
from viewmodels.StudyResearcherListViewModel import StudyResearcherListViewModel
from viewmodels.StudyResearcherViewModel import StudyResearcherViewModel
from viewmodels.VisitListViewModel import VisitListViewModel
from viewmodels import EventListViewModel
from views.StudyResearcherPanel import StudyResearcherPanel
from views.StudyVisitPanel import StudyVisitPanel
from views.EventPanel import EventPanel


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    return None


class StudyEditor(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study = Study.empty()

    async def save(self):
        await self.vm.call("save_study")

    async def load(self, study: Study):
        self.study = study
        await self.vm.call("copy", study=study)

    def patient_panel(self):
        panel = StudyPatientPanel(PatientListViewModel())
        panel.show()

    def researcher_panel(self):
        panel = StudyResearcherPanel(StudyResearcherListViewModel())
        panel.show()

    def visit_panel(self):
        panel = StudyVisitPanel(VisitListViewModel())
        panel.show()

    def monitoring_panel(self):
        panel = StudyMonitoringPanel(MonitoringListViewModel())
        panel.show()

    def adverse_events_panel(self):
        panel = EventPanel(EventListViewModel())
        panel.show()

    def study_pane(self):
        with ui.row().classes("mt-2 w-full"):
            ui.button("New",
                      on_click=lambda: self.load(Study.empty())) \
                .props("icon=add") \
                .classes("text-xs")

            ui.button("Save", on_click=lambda: self.save()) \
                .props("icon=save") \
                .classes("text-xs") \
                .disable() \
                .bind_enabled(self.vm, "data_changed")

            ui.button("Undo", on_click=lambda: self.load(self.study)) \
                .props("icon=undo") \
                .classes("text-xs")

            ui.space()

            ui.button("Delete", on_click=lambda: ui.notify("Study deleted")) \
                .classes("text-xs mr-2") \
                .props("icon=delete") \
                 \
                .disable()

        ui.input(label="Name", validation=validate_name,
                 on_change=lambda: self.vm.call("mark_changed", field_name="name")) \
             .classes("w-full") \
             .bind_value(self.vm, "name")

        ui.input(label="Sponsor",
                 on_change=lambda: self.vm.call("mark_changed", field_name="sponsor")) \
             .classes("w-full") \
             .bind_value(self.vm, "sponsor")

        with ui.row().classes("gap-2"):
            ui.date_input(label="Start Date",
                          on_change=lambda: self.vm.call("mark_changed", field_name="start_date")) \
                .bind_value(self.vm, "start_date")
            ui.date_input(label="End Date",
                          on_change=lambda: self.vm.call("mark_changed", field_name="end_date")) \
                .bind_value(self.vm, "end_date")

        with ui.row().classes("gap-2"):
            ui.number(label="Protocol Visits", value=1,
                      on_change=lambda: self.vm.call("mark_changed", field_name="visits")) \
                 .props('clearable') \
                 .classes("w-full") \
                 .bind_value(self.vm, "visits", strict=True)

        with ui.row().classes("gap-2 w-full"):
            ui.textarea(label="Comments",
                        on_change=lambda: self.vm.call("mark_changed", field_name="comments")) \
                 .classes("w-full") \
                 .bind_value(self.vm, "comments")

    def details_pane(self):
        with ui.tabs().props("horizontal").classes("p-0").bind_visibility(self.vm, "is_old") as tabs:
            visits = ui.tab("Visits", icon="event").classes("text-sky-800")
            monitoring = ui.tab("Monitoring", icon="monitor_heart").classes("text-sky-800")
            adverse_events = ui.tab("Events", icon="dangerous").classes("text-sky-800")
            patients = ui.tab("Patients", icon="personal_injury").classes("text-sky-800")
            researchers = ui.tab("Researchers", icon="group").classes("text-sky-800")
        with (ui.tab_panels(tabs, value=visits)
                .classes("size-full")):
            with (ui.tab_panel(visits)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.visit_panel()

            with (ui.tab_panel(monitoring)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.monitoring_panel()

            with (ui.tab_panel(adverse_events)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.adverse_events_panel()

            with (ui.tab_panel(patients)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.patient_panel()

            with (ui.tab_panel(researchers)
                    .classes("pl-2 pt-0 pb-0 pr-0")
                    .bind_visibility(self.vm, "is_old")):
                self.researcher_panel()

    def show(self):
        with ui.splitter(value=35).classes("w-full") as splitter:
            with splitter.before:
                self.study_pane()
            with splitter.after:
                self.details_pane()
