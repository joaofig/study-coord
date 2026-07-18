from nicegui import ui

from src.viewmodels import PatientViewModel
from src.viewmodels.view_model import ViewModel
from src.views.StudyPatientGrid import StudyPatientGrid
from src.views.dialogs.StudyPatientDialog import StudyPatientDialog
from src.views.View import View
from src.views.dialogs.DeleteWarningDialog import DeleteWarningDialog
from src.tools.excel import export_to_excel


class StudyPatientPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._study_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _new_patient_dialog(self):
        patient_vm = PatientViewModel()
        patient_vm.study_id = self.study_id
        dialog = StudyPatientDialog(patient_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    async def _on_delete_patient(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this patient?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            patient_id = self.vm.get("patient_id")
            await self.vm.call("delete_patient", patient_id=patient_id)
            await self.vm.call("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-none pl-0"):
                with ui.button(icon="add", on_click=lambda: self._new_patient_dialog()) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add Patient")

                with ui.button(icon="delete", on_click=lambda: self._on_delete_patient()) \
                        .bind_enabled(self.vm, "patient_id") \
                        .classes("text-xs") \
                        .props("color=red padding=xs"):
                    ui.tooltip("Delete Patient")

                with ui.button(icon="table_view",
                               on_click=lambda: export_to_excel(self.vm.get("patients"), "patients.xlsx")) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                StudyPatientGrid(self.vm).show()
