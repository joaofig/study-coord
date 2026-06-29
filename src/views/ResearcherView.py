from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.ResearcherGrid import ResearcherGrid
from views.View import View


class ResearcherView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-1"):
                self.grid = ResearcherGrid(vm)

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add"):
                    ui.tooltip("Add Researcher")

                with ui.button(icon="delete"):
                    ui.tooltip("Delete Researcher")

                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")

    async def _handle_notification(self, action: str, **kwargs):
        ...
