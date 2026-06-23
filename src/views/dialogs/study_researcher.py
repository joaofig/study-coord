from nicegui import ui

from viewmodels.view_model import ViewModel


def validate_patient_number(value: str | None) -> str | None:
    if not value:
        return "Patient number is required"
    return None


class StudyResearcherDialog:
    def __init__(self, vm: ViewModel):
        self.vm = vm

    async def show(self):
        with ui.dialog() as dialog, ui.card():
            ui.label("Study Researcher Details").classes("text-base")

            (ui.input("Number", validation=validate_patient_number)
                 .classes("w-full")
                 .bind_value(self.vm, "number")
            )

            (ui.input("Name")
                 .classes("w-full")
                 .bind_value(self.vm, "name")
            )

            (ui.textarea("Comments")
                 .classes("w-full")
                 .bind_value(self.vm, "comments")
            )
            with ui.row():
                ui.button("Save", on_click=lambda: dialog.submit("save"))
                ui.button("Close", on_click=lambda: dialog.submit("close"))
        return await dialog
