from nicegui import ui

from src.viewmodels import PatientViewModel
from src.viewmodels.ViewModel import ViewModel
from src.views.StudyPatientGrid import StudyPatientGrid
from src.views.dialogs.StudyPatientDialog import StudyPatientDialog
from src.views.View import View
from tools.messenger import get_messenger


class StudyPatientPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.study_messenger = get_messenger("study")
        self.study_messenger.subscribe("study_selected", self._study_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _new_patient_dialog(self):
        patient_vm = PatientViewModel()
        patient_vm.study_id = self.study_id
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm_message("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-1"):
                StudyPatientGrid(self.vm).show()

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=lambda: self._new_patient_dialog()):
                    ui.tooltip("Add Patient")

                # with ui.button(icon="edit", on_click=lambda: self.edit_patient_dialog()):
                #     ui.tooltip("Edit Patient")

                with ui.button(icon="delete"):
                    ui.tooltip("Delete Patient")

                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")
