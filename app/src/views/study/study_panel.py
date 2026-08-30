from nicegui import ui
from src.viewmodels import (
    MonitoringListViewModel,
    PatientListViewModel,
    ProtocolListViewModel,
)
from src.viewmodels.study.study_researcher_list import StudyResearcherListViewModel
from src.viewmodels.timeline import TimelineViewModel
from nicemvvm.viewmodels.view_model import ViewModel
from src.views.study.monitorization_panel import StudyMonitorizationPanel
from src.views.study.patient_detail_panel import PatientDetailPanel
from src.views.study.patient_panel import StudyPatientPanel
from src.views.study.protocol_panel import ProtocolPanel
from src.views.study.study_researcher_panel import StudyResearcherPanel
from src.views.timeline_panel import TimelinePanel
from nicemvvm.views.view import View


class StudyPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_detail_panel()

    def patient_panel(self):
        with ui.splitter(value=50).classes("w-full h-full") as splitter:
            with splitter.before:
                patient_vm = PatientListViewModel()
                panel = StudyPatientPanel(patient_vm)
                panel.show()
            with splitter.after:  # as splitter_right:
                PatientDetailPanel(self.vm, patient_vm)

    def study_detail_panel(self):
        with (
            ui.tabs()
            .props("dense no-caps")
            .bind_visibility(self.vm, "selected_id") as tabs
        ):
            patients = ui.tab("Patients").classes("text-sky-800")
            monitoring = ui.tab("Monitoring Visits").classes("text-sky-800")
            researchers = ui.tab("Researchers").classes("text-sky-800")
            protocols = ui.tab("Protocol Deviations").classes("text-sky-800")
            timeline = ui.tab("Timeline").classes("text-sky-800")

        with ui.tab_panels(tabs, value=patients, animated=False).classes(
            "w-full h-full"
        ):
            with (
                ui.tab_panel(patients)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                self.patient_panel()

            with (
                ui.tab_panel(monitoring)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                StudyMonitorizationPanel(MonitoringListViewModel())

            with (
                ui.tab_panel(researchers)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                StudyResearcherPanel(StudyResearcherListViewModel())

            with (
                ui.tab_panel(protocols)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                ProtocolPanel(ProtocolListViewModel())

            with (
                ui.tab_panel(timeline)
                .classes("pl-0 pt-0 pb-0 pr-0")
                .bind_visibility(self.vm, "selected_id")
            ):
                TimelinePanel(TimelineViewModel())
