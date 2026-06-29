from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from viewmodels import ResearcherViewModel
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
        self.dialog = None

        with ui.dialog() as dialog, ui.card().classes("w-100"):
            ui.label("Researcher Details").classes("text-h5")
            self.number = ui.input(
                label="Number",
                validation = validate_number,
            ).classes("w-full")
            self.name = ui.input(label="Name").classes("w-full")
            ui.input(label="Phone").classes("w-full")
            ui.input(label="Email").classes("w-full")
            ui.textarea(label="Comments").classes("w-full")

            with ui.row():
                ui.button(
                    "Save",
                    on_click=lambda: self.handle_save()
                )
                ui.button("Cancel", on_click=lambda: dialog.submit("Cancel"))
            self.dialog = dialog

    def validate(self) -> bool:
        if not self.number.value:
            ui.notify("Number is required", color="negative")
            return False
        return True

    def handle_save(self):
        if self.validate():
            self.dialog.submit("Save")

    async def show(self):
        result = await self.dialog
        ui.notify(f'You chose {result}')


async def show_dialog():
    dialog = ResearcherDialog(ResearcherViewModel())
    await dialog.show()


