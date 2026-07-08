from nicegui import ui
from nicegui.elements.row import Row
from nicegui.events import ValueChangeEventArguments

from viewmodels import PatientListViewModel, MonitoringListViewModel, ProtocolListViewModel, VisitListViewModel, \
    EventListViewModel
from viewmodels.StudyResearcherListViewModel import StudyResearcherListViewModel
from viewmodels.ViewModel import ViewModel
from views.EventPanel import EventPanel
from views.StudyMonitoringPanel import StudyMonitoringPanel
from views.StudyPatientPanel import StudyPatientPanel
from views.StudyResearcherPanel import StudyResearcherPanel
from views.ProtocolPanel import ProtocolPanel
from views.StudyVisitPanel import StudyVisitPanel
from views.View import View


class StudyPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        with ui.splitter(value=50).classes("w-full h-full") as splitter:
            with splitter.after:
                self.container = self.details_pane()

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
        panel = EventPanel(EventListViewModel())
        panel.show()

    def patient_detail_panel(self):
        with ui.tabs().props("dense no-caps") as tabs:
            visits = ui.tab("Visits").classes("text-sky-800")
            events = ui.tab("Events").classes("text-sky-800")
        with ui.tab_panels(tabs, value=visits).classes("w-full h-full"):
            with ui.tab_panel(visits) \
                    .classes("pl-0 pt-0 pb-0 pr-0"):
                self.visits_panel()

            with ui.tab_panel(events) \
                    .classes("pl-0 pt-0 pb-0 pr-0"):
                self.events_panel()

    def on_tab_change(self, tab: ValueChangeEventArguments):
        if tab.value == "Patients":
            with self.container:
                self.patient_detail_panel()
        else:
            self.container.clear()

    def study_pane(self):
        with ui.tabs(on_change=self.on_tab_change) \
                .props("dense no-caps") as tabs:
            patients = ui.tab("Patients").classes("text-sky-800")
            monitoring = ui.tab("Monitoring").classes("text-sky-800")
            researchers = ui.tab("Researchers").classes("text-sky-800")
            protocols = ui.tab("Protocol").classes("text-sky-800")

        with ui.tab_panels(tabs, value=patients).classes("w-full h-full"):
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

    def details_pane(self) -> Row:
        return ui.row().classes("w-full h-full p-0 m-0")
