from nicegui import ui

from tools.messenger import get_messenger
from viewmodels.ViewModel import ViewModel
from views.StudyResearcherGrid import StudyResearcherGrid
from views.View import View


class StudyResearcherPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.study_messenger = get_messenger("study_researcher")
        self.study_messenger.subscribe("study_researcher_selected", self._study_researcher_selected)

    async def _study_researcher_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    def show(self):
        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-1"):
                StudyResearcherGrid(self.vm).show()
            with ui.column().classes("h-full flex-none"):

                with ui.button(icon="add"):
                    ui.tooltip("Add Researcher")

                with ui.button(icon="delete"):
                    ui.tooltip("Delete Researcher")

                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")
