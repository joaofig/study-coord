from nicegui import ui

from src.viewmodels.MonitoringViewModel import MonitoringViewModel
from src.viewmodels.ViewModel import ViewModel
from src.views.StudyMonitoringGrid import StudyMonitoringGrid
from src.views.dialogs.StudyMonitoringDialog import StudyMonitoringDialog
from src.views.View import View
from src.views.dialogs.DeleteWarningDialog import DeleteWarningDialog
from src.tools.excel import export_to_excel


class StudyMonitoringPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._study_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _new_monitoring_dialog(self):
        monitoring_vm = MonitoringViewModel()
        monitoring_vm.study_id = self.study_id
        dialog = StudyMonitoringDialog(monitoring_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    async def _on_delete_monitoring(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this monitoring visit?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            monitoring_id = self.vm.get("monitoring_id")
            await self.vm.call("delete_monitoring", monitoring_id=monitoring_id)
            await self.vm.call("load", study_id=self.study_id)
            await self.broadcast("study_list", "load")

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-none pl-0"):
                with ui.button(icon="add", on_click=lambda: self._new_monitoring_dialog()) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add Monitoring Visit")

                with ui.button(icon="delete", on_click=lambda: self._on_delete_monitoring()) \
                        .bind_enabled(self.vm, "monitoring_id") \
                        .classes("text-xs") \
                        .props("color=red padding=xs"):
                    ui.tooltip("Delete Monitoring Visit")

                with ui.button(icon="table_view",
                               on_click=lambda: export_to_excel(self.vm.get("monitorings"), "monitorings.xlsx")) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                StudyMonitoringGrid(self.vm).show()
