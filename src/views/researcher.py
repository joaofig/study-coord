from nicegui import ui
from nicegui.elements.aggrid import AgGrid


def validate_number(value: str) -> str | None:
    if not value:
        return "Number is required"
    return None


class ResearcherDialog:
    def __init__(self):
        self.number = None
        self.name = None
        self.dialog = None

        with ui.dialog() as dialog, ui.card():
            ui.label("Researcher Details").classes("text-h5")
            self.number = ui.input(
                label="Number",
                validation = validate_number,
            ).classes("w-full")
            self.name = ui.input(label="Name").classes("w-full")

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
    dialog = ResearcherDialog()
    await dialog.show()


def researcher_grid() -> AgGrid:
    columns = [
        {"headerName": "ID", "field": "id", "hide": True},
        {"headerName": "Number", "field": "sponsor", "sortable": True, "align": "left"},
        {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
    ]
    grid_def = {
        "columnDefs": columns,
        "rowData": []
    }
    return ui.aggrid(grid_def)


def researcher_grid_view():
    with ui.row().classes("w-full"):
        ui.label("Researchers").classes("text-h4")
        ui.space()
        ui.button("Add Researcher", on_click=lambda: show_dialog()).props("icon=add")
    with ui.row().classes("w-full h-full"):
        researcher_grid().classes("h-full")
