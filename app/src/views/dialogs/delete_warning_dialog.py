from nicegui import ui


class DeleteWarningDialog:
    def __init__(self, message: str):
        with ui.dialog() as dialog, ui.card():
            with ui.row():
                ui.icon("warning", color="red", size="md")
                ui.label("Warning").classes("text-lg font-bold")
            with ui.row():
                ui.label(message)
            with ui.row().classes("justify-end"):
                ui.button("Delete", on_click=lambda: dialog.submit("delete")).props(
                    "color=red"
                )
                ui.button("Cancel", on_click=dialog.close)
            self.dialog = dialog

    async def show(self):
        result = await self.dialog
        return result

    def close(self):
        self.dialog.close()
