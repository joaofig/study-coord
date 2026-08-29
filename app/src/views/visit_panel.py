from nicegui import ui
from nicemvvm.tools.excel import export_to_excel
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from src.viewmodels.visit import VisitViewModel
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.visit_dialog import StudyVisitDialog
from nicemvvm.views.view import View
from src.views.visit_grid import StudyVisitGrid


class StudyVisitPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.patient_id = 0
        self.subscribe(
            channel="study", message="selected", handler=self._study_selected
        )
        self.subscribe(
            channel="patient", message="selected", handler=self._patient_selected
        )

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with (
                    ui.button(icon="add", on_click=self._new_visit_dialog)
                    .classes("text-xs")
                    .props("padding=xs")
                    .set_enabled(not is_user_readonly())
                ):
                    ui.tooltip("Add Visit")

                with (
                    ui.button(icon="delete", on_click=self._on_delete_visit)
                    .bind_enabled(self.vm, "selected_id")
                    .classes("text-xs")
                    .props("padding=xs color=red")
                ):
                    ui.tooltip("Delete Visit")

                with (
                    ui.button(
                        icon="table_view",
                        on_click=lambda: export_to_excel(
                            self.vm.get("visits"), "visits.xlsx"
                        ),
                    )
                    .classes("text-xs")
                    .props("padding=xs")
                    .set_enabled(not is_user_readonly())
                ):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                StudyVisitGrid(self.vm).show()

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
        if not is_user_readonly():
            dialog = DeleteWarningDialog("Are you sure you want to delete this visit?")
            result = await dialog.show()
            if result == "delete":
                dialog.close()
                visit_id = self.vm.get("selected_id")
                if visit_id:
                    await self.vm.call("delete", visit_id=visit_id)
        else:
            ui.notify("You do not have permission to delete visits", type="negative")
