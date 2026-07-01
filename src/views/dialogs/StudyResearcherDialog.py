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
        self.vm = vm

        with ui.dialog() as dialog, ui.card():
            ui.label("Study Researcher Details").classes("text-base")

            ui.label("Researcher:")
            self.select = ui.select(options=self.vm.get("researchers"), label="Researcher") \
                .bind_value(self.vm, "researcher_id") \
                .on_value_change(self._on_select_change)

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
                ui.button("Save", on_click=lambda: dialog.submit("save"))
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    def _on_select_change(self, event):
        pass

    async def _handle_notification(self, action: str, **kwargs):
        match action:
            case "save":
                researcher = self.vm.get("researcher")
                researcher.name = self.select.value
                await self.vm.save()
                await self.dialog.submit("close")

            case "researcher_list_loaded":
                self.select.set_options(self.vm.get("researchers"))


    async def show(self):
        return await self.dialog

    async def _on_dialog_submit(self, action: str):
        if action == "save":
            await self.vm_message("save")
        await self.dialog.close()