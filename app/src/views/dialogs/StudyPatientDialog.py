from nicegui import ui
from nicegui.elements.dialog import Dialog

from src.viewmodels.view_model import ViewModel
from src.views.View import View


def validate_patient_number(value: str | None) -> str | None:
    if not value:
        return "Patient number is required"
    return None


class StudyPatientDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.dialog: Dialog = self._build_dialog()

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")

    async def show(self):
        return await self.dialog

    def _build_dialog(self) -> Dialog:
        statuses = self.vm.get("statuses")
        with ui.dialog() as dialog, ui.card():
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Patient Details").classes("text-base")

            (ui.input("Number", validation=validate_patient_number)
                 .classes("w-full")
                 .bind_value(self.vm, "number")
            )
            (ui.input("Name")
                 .classes("w-full")
                 .bind_value(self.vm, "name")
            )
            with ui.row():
                (ui.date_input("Start Date")
                     .bind_value(self.vm, "start_date")
                )
                (ui.date_input("Exit Date")
                     .bind_value(self.vm, "exit_date")
                )
            (ui.select(options=statuses, label="Status", value="active")
                 .classes("w-full")
                 .bind_value(self.vm, "status")
            )
            (ui.textarea("Comments")
                 .classes("w-full")
                 .bind_value(self.vm, "comments")
            )
            with ui.row():
                ui.button("Save", on_click=lambda: self.save())
                ui.button("Close", on_click=lambda: dialog.submit("close"))
        return dialog
