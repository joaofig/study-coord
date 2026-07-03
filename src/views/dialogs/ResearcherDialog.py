from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.View import View


def validate_number(value: str) -> str | None:
    if not value:
        return "Number is required"
    return None


class ResearcherDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.number = None
        self.name = None

        with ui.dialog() as dialog, ui.card().classes("w-100"):
            ui.label("Researcher Details").classes("text-h5")
            self.number = ui.input(
                label="Number",
                validation = validate_number,
            ).classes("w-full").bind_value(self.vm, "number")
            self.name = ui.input(label="Name").classes("w-full").bind_value(self.vm, "name")
            ui.input(label="Phone").classes("w-full").bind_value(self.vm, "phone")
            ui.input(label="Email").classes("w-full").bind_value(self.vm, "email")
            ui.textarea(label="Comments").classes("w-full").bind_value(self.vm, "comments")

            with ui.row():
                ui.button(
                    "Save",
                    on_click=lambda: self.save()
                )
                ui.button("Cancel", on_click=lambda: dialog.submit("cancel"))
            self.dialog = dialog

    async def save(self):
        await self.vm_message("save")
        self.dialog.submit("save")

    def validate(self) -> bool:
        if not self.number.value:
            ui.notify("Number is required", color="negative")
            return False
        return True

    async def show(self):
        return await self.dialog
