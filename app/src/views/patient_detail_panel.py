from nicegui import ui
from src.viewmodels import AdverseEventListViewModel, ViewModel, VisitListViewModel
from src.views.event_panel import EventPanel
from nicemvvm.views.view import View
from src.views.visit_panel import StudyVisitPanel


class PatientDetailPanel(View):
    def __init__(self, vm: ViewModel, patient_vm: ViewModel):
        super().__init__(vm)

        with (
            ui.column()
            .classes("h-full w-full p-0")
            .bind_visibility(patient_vm, "selected_id") as container
        ):
            ui.separator()
            with (
                ui.tabs()
                .props("dense no-caps")
                .bind_visibility(self.vm, "selected_id") as tabs
            ):
                visits = ui.tab("Visits").classes("text-sky-800")
                events = ui.tab("Adverse Events").classes("text-sky-800")

            with ui.tab_panels(tabs, value=visits, animated=False).classes(
                "w-full h-full"
            ):
                with ui.tab_panel(visits).classes("pl-4 pt-0 pb-0 pr-0"):
                    StudyVisitPanel(VisitListViewModel())

                with ui.tab_panel(events).classes("pl-4 pt-0 pb-0 pr-0"):
                    EventPanel(AdverseEventListViewModel())
