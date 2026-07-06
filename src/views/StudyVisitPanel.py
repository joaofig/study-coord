from nicegui import ui

from viewmodels.ViewModel import ViewModel
from viewmodels.VisitViewModel import VisitViewModel
from views.StudyVisitGrid import StudyVisitGrid
from views.View import View
from views.dialogs.DeleteWarningDialog import DeleteWarningDialog
from views.dialogs.StudyVisitDialog import StudyVisitDialog


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

    async def _new_visit_dialog(self):
        visit_vm = VisitViewModel()
        await visit_vm.load_patients(self.study_id)
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

            with ui.column().classes("h-full flex-1"):
                StudyVisitGrid(self.vm).show()

            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=self._new_visit_dialog):
                    ui.tooltip("Add Visit")

                with ui.button(icon="delete", on_click=self._on_delete_visit) \
                        .bind_enabled(self.vm, "visit_id") \
                        .props("color=red"):
                    ui.tooltip("Delete Visit")

                with ui.button(icon="table_view"):
                    ui.tooltip("Export to Excel")
