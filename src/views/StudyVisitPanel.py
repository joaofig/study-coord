from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.StudyVisitGrid import StudyVisitGrid
from views.View import View


class StudyVisitPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.subscribe(channel="study",
                       message="study_selected",
                       handler=self._study_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-1"):
                StudyVisitGrid(self.vm).show()

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add"):
                    ui.tooltip("Add Patient")

                # with ui.button(icon="edit", on_click=lambda: self.edit_patient_dialog()):
                #     ui.tooltip("Edit Patient")

                with ui.button(icon="delete"):
                    ui.tooltip("Delete Patient")

                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")
        return self.grid