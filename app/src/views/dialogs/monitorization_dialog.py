from nicegui import ui
from nicegui.elements.dialog import Dialog

from src.tools.user import is_user_readonly
from src.viewmodels.view_model import ViewModel
from src.views.view import View


class StudyMonitorizationDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.dialog: Dialog = self._build_dialog()

    async def save(self):
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")

    async def show(self):
        return await self.dialog

    def _build_dialog(self) -> Dialog:
        with ui.dialog() as dialog, ui.card().classes("w-120"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Monitorization Visit Details").classes("text-base")

            (
                ui.date_input("Date")
                .classes("w-full")
                .props("dense")
                .bind_value(self.vm, "meeting_date")
            )
            (
                ui.input("Monitor")
                .classes("w-full")
                .props("dense")
                .bind_value(self.vm, "monitor")
            )
            (ui.textarea("Comments").classes("w-full").props("dense").bind_value(self.vm, "comments"))

            ui.markdown().classes("bg-orange-200 w-full") \
                .bind_content_from(self.vm, "validation") \
                .bind_visibility_from(self.vm, "is_invalid")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save()) \
                    .props("dense") \
                    .set_enabled(not is_user_readonly())
                ui.button("Close", on_click=lambda: dialog.submit("close")).props("dense")
        return dialog
