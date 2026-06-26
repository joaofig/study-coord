from nicegui import ui

from tools.messenger import get_messenger
from viewmodels.PatientViewModel import PatientListViewModel, PatientViewModel
from viewmodels.ViewModel import ViewModel
from views.StudyPatientGrid import StudyPatientGrid
from views.dialogs.StudyPatientDialog import StudyPatientDialog
from views.View import View


class PatientPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.vm = PatientListViewModel()
        self.messenger = get_messenger("patient")
        self.messenger.subscribe("study_selected", self._handle_study_selected)

    async def _handle_study_selected(self, **args):
        study_id = args.get("study_id")
        if study_id:
            await self.vm.load_patients(study_id)
            self._update_grid()

    async def show_patient_dialog(self):
        patient_vm = PatientViewModel()
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()
        if result == "save":
            await self.messenger.send("saved", patient_vm.to_dict())

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-1"):
                StudyPatientGrid(self.vm).show()

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=lambda: self.show_patient_dialog()):
                    ui.tooltip("Add Patient")
                with ui.button(icon="delete"):
                    ui.tooltip("Delete Patient")
                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")