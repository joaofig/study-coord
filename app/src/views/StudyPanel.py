from nicegui import ui
from nicegui.events import ValueChangeEventArguments

from src.viewmodels import PatientListViewModel, MonitoringListViewModel, ProtocolListViewModel, VisitListViewModel, AdverseEventListViewModel
from src.viewmodels.study_researcher_list import StudyResearcherListViewModel
from src.viewmodels.view_model import ViewModel
from src.views.EventPanel import EventPanel
from src.views.StudyMonitoringPanel import StudyMonitoringPanel
from src.views.patient_panel import StudyPatientPanel
from src.views.StudyResearcherPanel import StudyResearcherPanel
from src.views.protocol_panel import ProtocolPanel
from src.views.StudyVisitPanel import StudyVisitPanel
from src.views.View import View


class StudyPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.children = {}

        with ui.splitter(value=50).classes("w-full h-full") as splitter:

            with splitter.after: # as splitter_right:
                self.patient_detail_panel()
                # self.container = ui.column().classes("h-full w-full pl-0 pt-0 pb-0 pr-0")

            with splitter.before:
                self.study_pane()

    def patient_panel(self):
        panel = StudyPatientPanel(PatientListViewModel())
        panel.show()

    def monitoring_panel(self):
        panel = StudyMonitoringPanel(MonitoringListViewModel())
        panel.show()

    def researcher_panel(self):
        panel = StudyResearcherPanel(StudyResearcherListViewModel())
        panel.show()

    def protocol_panel(self):
        panel = ProtocolPanel(ProtocolListViewModel())
        panel.show()

    def visits_panel(self):
        panel = StudyVisitPanel(VisitListViewModel())
        panel.show()

    def events_panel(self):
        panel = EventPanel(AdverseEventListViewModel())
        panel.show()

    def patient_detail_panel(self):
        with ui.column().classes("h-full w-full pl-0 pt-0 pb-0 pr-0") as container:
            with ui.tabs().props("dense no-caps") \
                    .bind_visibility(self.vm, "selected_id") as tabs:
                visits = ui.tab("Visits").classes("text-sky-800")
                events = ui.tab("Events").classes("text-sky-800")
            with ui.tab_panels(tabs, value=visits, animated=False).classes("w-full h-full"):
                with ui.tab_panel(visits) \
                        .bind_visibility(self.vm, "selected_id") \
                        .classes("pl-4 pt-0 pb-0 pr-0"):
                    self.visits_panel()

                with ui.tab_panel(events) \
                        .bind_visibility(self.vm, "selected_id") \
                        .classes("pl-4 pt-0 pb-0 pr-0"):
                    self.events_panel()
        self.children["Patients"] = container
        container.set_visibility(False)

    def on_tab_change(self, tab: ValueChangeEventArguments):
        for (name, view) in self.children.items():
            view.set_visibility(name == tab.value)

    def study_pane(self):
        with ui.tabs(on_change=self.on_tab_change) \
                .props("dense no-caps") \
                .bind_visibility(self.vm, "selected_id") as tabs:
            patients = ui.tab("Patients").classes("text-sky-800")
            monitoring = ui.tab("Monitoring").classes("text-sky-800")
            researchers = ui.tab("Researchers").classes("text-sky-800")
            protocols = ui.tab("Protocol").classes("text-sky-800")

        with ui.tab_panels(tabs, value=patients, animated=False).classes("w-full h-full"):
            with ui.tab_panel(patients) \
                    .classes("pl-0 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.patient_panel()

            with ui.tab_panel(monitoring) \
                    .classes("pl-0 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.monitoring_panel()

            with ui.tab_panel(researchers) \
                    .classes("pl-0 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.researcher_panel()

            with ui.tab_panel(protocols) \
                    .classes("pl-0 pt-0 pb-0 pr-0") \
                    .bind_visibility(self.vm, "selected_id"):
                self.protocol_panel()
