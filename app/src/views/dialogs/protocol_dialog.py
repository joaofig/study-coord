from nicegui import ui
from nicegui.elements.dialog import Dialog

from src.viewmodels.view_model import ViewModel
from src.views.view import View


def validate_title(value: str | None) -> str | None:
    if not value:
        return "Title is required"
    return None


class ProtocolDialog(View):
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
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("Protocol Deviation Details").classes("text-base")

            ui.input("Title", validation=validate_title).classes("w-full").bind_value(
                self.vm, "title"
            )

            ui.date_input("Date").classes("w-full").bind_value(self.vm, "event_date")

            ui.textarea("Description").classes("w-full").bind_value(
                self.vm, "description"
            )

            ui.markdown().classes("bg-orange-200 w-full") \
                .bind_content_from(self.vm, "validation") \
                .bind_visibility_from(self.vm, "is_invalid")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save())
                ui.button("Close", on_click=lambda: dialog.submit("close"))
        return dialog
