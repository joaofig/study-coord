from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.View import View


def validate_patient_number(value: str | None) -> str | None:
    if not value:
        return "Researcher number is required"
    return None


class StudyResearcherDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-100"):
            ui.label("Study Researcher Details").classes("text-base")

            self.select = ui.select(options=self.vm.get("researchers"), label="Researcher") \
                .bind_value(self.vm, "researcher_id") \
                .on_value_change(self._on_select_change) \
                .classes("w-full")

            selection = self.vm.get("selection")
            ui.input(label="Number").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "number")
            ui.input(label="Name").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "name")
            ui.input(label="Phone").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "phone")
            ui.input(label="Email").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "email")

            with ui.row():
                ui.button("Save", on_click=self.save)
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    async def _on_select_change(self, event):
        await self.vm_message("researcher_id", value=event.value)

    async def _handle_notification(self, action: str, **kwargs):
        print(action)
        match action:
            case "researcher_list_loaded":
                researcher_id = self.vm.get("researcher_id")
                print(researcher_id)
                self.select.set_options(self.vm.get("researchers"), value=researcher_id)
            case "researcher_saved":
                self.dialog.submit("save")

    async def save(self):
        await self.vm_message("save")

    async def show(self):
        return await self.dialog
