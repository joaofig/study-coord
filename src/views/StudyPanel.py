from nicegui import ui

from viewmodels import PatientListViewModel, MonitoringListViewModel
from viewmodels.StudyResearcherListViewModel import StudyResearcherListViewModel
from viewmodels.ViewModel import ViewModel
from views.StudyMonitoringPanel import StudyMonitoringPanel
from views.StudyPatientPanel import StudyPatientPanel
from views.StudyResearcherPanel import StudyResearcherPanel
from views.View import View


class StudyPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

    def show(self):
        with ui.splitter(value=50).classes("w-full") as splitter:
            with splitter.before:
                self.study_pane()

            with splitter.after:
                self.details_pane()

    def patient_panel(self):
        panel = StudyPatientPanel(PatientListViewModel())
        panel.show()

    def monitoring_panel(self):
        panel = StudyMonitoringPanel(MonitoringListViewModel())
        panel.show()

    def researcher_panel(self):
        panel = StudyResearcherPanel(StudyResearcherListViewModel())
        panel.show()

    def study_pane(self):
        with ui.tabs().classes("p-0").props("dense no-caps") as tabs:
            patients = ui.tab("Patients").classes("text-sky-800")
            monitoring = ui.tab("Monitoring").classes("text-sky-800")
            researchers = ui.tab("Researchers").classes("text-sky-800")

        with ui.tab_panels(tabs, value=patients).classes("w-full h-full"):
            with ui.tab_panel(patients) \
                    .classes("pl-2 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.patient_panel()

            with ui.tab_panel(monitoring) \
                    .classes("pl-2 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.monitoring_panel()

            with ui.tab_panel(researchers) \
                    .classes("pl-2 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.researcher_panel()

    def details_pane(self):
        return ui.row().classes("w-full h-full p-0 m-0")
