from nicegui import ui

from src.viewmodels import ProtocolViewModel
from src.viewmodels.view_model import ViewModel
from src.views.ProtocolGrid import ProtocolGrid
from src.views.dialogs.ProtocolDialog import ProtocolDialog
from src.views.View import View
from src.views.dialogs.DeleteWarningDialog import DeleteWarningDialog
from src.tools.excel import export_to_excel


class ProtocolPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.subscribe(channel="study",
                       message="selected",
                       handler=self._study_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _new_protocol_dialog(self):
        protocol_vm = ProtocolViewModel()
        protocol_vm.study_id = self.study_id
        dialog = ProtocolDialog(protocol_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=self.study_id)

    async def _on_delete_protocol(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this protocol deviation?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            protocol_id = self.vm.get("protocol_id")
            await self.vm.call("delete_protocol", protocol_id=protocol_id)
            await self.vm.call("load", study_id=self.study_id)

    def show(self):
        with ui.row().classes("w-full h-full"):

            with ui.column().classes("h-full flex-none pl-0"):
                with ui.button(icon="add", on_click=lambda: self._new_protocol_dialog()) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add Protocol Deviation")

                with ui.button(icon="delete", on_click=lambda: self._on_delete_protocol()) \
                        .bind_enabled(self.vm, "protocol_id") \
                        .classes("text-xs") \
                        .props("color=red padding=xs"):
                    ui.tooltip("Delete Protocol Deviation")

                with ui.button(icon="table_view",
                               on_click=lambda: export_to_excel(self.vm.get("protocols"), "protocols.xlsx")) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                ProtocolGrid(self.vm).show()
