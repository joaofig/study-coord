from nicegui import ui

from src.tools.messenger import get_messenger
from src.viewmodels import PatientViewModel
from src.viewmodels.ViewModel import ViewModel
from src.views.StudyPatientGrid import StudyPatientGrid
from src.views.dialogs.StudyPatientDialog import StudyPatientDialog
from src.views.View import View


class PatientPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

    async def show_patient_dialog(self):
        patient_vm = PatientViewModel()
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()
        if result == "save":
            await self.command("reload_patients")

    async def edit_patient_dialog(self):
        patient_vm = PatientViewModel()
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()
        if result == "save":
            await self.command("reload_patients")

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-1"):
                StudyPatientGrid(self.vm).show()

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=lambda: self.show_patient_dialog()):
                    ui.tooltip("Add Patient")

                with ui.button(icon="edit", on_click=lambda: self.edit_patient_dialog()):
                    ui.tooltip("Edit Patient")

                with ui.button(icon="delete"):
                    ui.tooltip("Delete Patient")

                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")