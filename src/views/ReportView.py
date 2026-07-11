from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.View import View


class ReportView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full"):
            self._add_count_card("Studies", "study_count")
            self._add_count_card("Patients", "patient_count")
            self._add_count_card("Researchers", "researcher_count")
            self._add_count_card("Visits", "visit_count")
            self._add_count_card("Events", "event_count")

        with ui.row().classes("w-full"):
            ui.button("Refresh", icon="change_circle", on_click=self._on_refresh)

    def _add_count_card(self, title: str, property_name: str):
        with ui.card().classes("bg-gray-200"):
            ui.label(title).classes("text-2xl")
            with ui.card_section().classes("w-full"):
                ui.label("0").bind_text_from(self.vm, property_name) \
                    .classes("text-xl text-right font-bold")

    async def _on_refresh(self):
        await self.vm.call("load")