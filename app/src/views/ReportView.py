from nicegui import ui
from nicegui.observables import ObservableDict

from src.viewmodels.view_model import ViewModel
from src.views.View import View


class ReportView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.studies = vm.get("studies")
        if isinstance(self.studies, ObservableDict):
            self.studies.on_change(self._update_selector)

        with ui.row().classes("w-full"):
            self._add_count_card("Studies", "study_count")
            self._add_count_card("Patients", "patient_count")
            self._add_count_card("Researchers", "researcher_count")
            self._add_count_card("Visits", "visit_count")
            self._add_count_card("Events", "event_count")

        with ui.row().classes("w-full"):
            ui.separator()

            studies = self.vm.get("studies")
            self.selector = ui.select(studies, label="Study", on_change=self._on_study_change) \
                .bind_value(self.vm, "study_id") \
                .classes("w-100")

        with ui.row().classes("w-full"):
            self._add_count_card("Patients", "study_patient_count")
            self._add_count_card("Researchers", "study_researcher_count")
            self._add_count_card("Visits", "study_visit_count")
            self._add_count_card("Events", "study_event_count")

        # with ui.row().classes("w-full"):
        #     ui.button("Refresh", icon="change_circle", on_click=self._on_refresh)

    def _add_count_card(self, title: str, property_name: str):
        with ui.card().classes("bg-gray-200"):
            ui.label(title).classes("text-2xl")
            with ui.card_section().classes("w-full"):
                ui.label("0").bind_text_from(self.vm, property_name) \
                    .classes("text-xl text-right font-bold text-sky-800")

    async def _on_refresh(self):
        await self.vm.call("load")

    async def _on_study_change(self):
        await self.vm.call("load_detail")

    def _update_selector(self, **kwargs):
        self.selector.set_options(self.studies)