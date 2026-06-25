from nicegui import ui

from tools.messenger import MessengerHub, Messenger
from viewmodels.patient import PatientListViewModel, PatientViewModel
from views.study_patient_grid import StudyPatientGrid
from views.dialogs.study_patient import StudyPatientDialog


class PatientPanel:
    def __init__(self):
        self.vm = PatientListViewModel()
        self.messenger = MessengerHub()["patient"]

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