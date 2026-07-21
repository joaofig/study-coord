from nicegui import ui

from src.tools.excel import export_to_excel
from src.viewmodels.view_model import ViewModel
from src.viewmodels.visit import VisitViewModel
from src.views.StudyVisitGrid import StudyVisitGrid
from src.views.View import View
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.study_visit_dialog import StudyVisitDialog


class StudyVisitPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.patient_id = 0
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._study_selected)
        self.subscribe(channel="patient",
                       message="selected",
                       handler=self._patient_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _patient_selected(self, **kwargs):
        if "patient_id" in kwargs:
            self.patient_id = kwargs["patient_id"]

    async def _new_visit_dialog(self):
        visit_vm = VisitViewModel()
        await visit_vm.load_patients(self.study_id)
        visit_vm.patient_id = self.patient_id
        await visit_vm.call("load_patient", patient_id=self.patient_id)
        dialog = StudyVisitDialog(visit_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    async def _on_delete_visit(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this visit?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            visit_id = self.vm.get("visit_id")
            if visit_id:
                await self.vm.call("delete_visit", visit_id=visit_id)
                # await self.vm.call("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=self._new_visit_dialog) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add Visit")

                with ui.button(icon="delete", on_click=self._on_delete_visit) \
                        .bind_enabled(self.vm, "visit_id") \
                        .classes("text-xs") \
                        .props("padding=xs color=red"):
                    ui.tooltip("Delete Visit")

                with ui.button(icon="table_view", on_click=lambda: export_to_excel(self.vm.get("visits"), "visits.xlsx")) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                StudyVisitGrid(self.vm).show()