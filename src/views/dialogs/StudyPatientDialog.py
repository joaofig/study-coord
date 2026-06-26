from nicegui import ui
from nicegui.elements.dialog import Dialog

from viewmodels.ViewModel import ViewModel


def validate_patient_number(value: str | None) -> str | None:
    if not value:
        return "Patient number is required"
    return None


class StudyPatientDialog:
    def __init__(self, vm: ViewModel):
        self.vm = vm

    async def save(self, dialog: Dialog):
        await self.vm.message("save")
        dialog.submit("save")

    async def show(self):
        statuses = self.vm.get("statuses")
        with ui.dialog() as dialog, ui.card():
            ui.label("Study Patient Details").classes("text-base")

            (ui.input("Number", validation=validate_patient_number)
                 .classes("w-full")
                 .bind_value(self.vm, "number")
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
                ui.button("Save", on_click=lambda: self.save(dialog))
                ui.button("Close", on_click=lambda: dialog.submit("close"))
        return await dialog
