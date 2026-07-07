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

        with ui.dialog() as dialog, ui.card().classes("w-120"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Researcher Details").classes("text-base")

            self.select = ui.select(options=self.vm.get("researchers"), label="Researcher") \
                .bind_value(self.vm, "researcher_id") \
                .on_value_change(lambda: self.vm.call(cmd="load")) \
                .classes("w-full")

            selection = self.vm.get("selection")
            ui.input(label="Number").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "number")
            ui.input(label="Phone").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "phone")
            ui.input(label="Email").props("readonly") \
                .classes("w-full") \
                .bind_value(selection, "email")

            self.select = ui.select(options=self.vm.get("roles"), label="Role") \
                .bind_value(self.vm, "role") \
                .classes("w-full")
            ui.textarea(label="Study Comments") \
                .classes("w-full") \
                .bind_value(self.vm, "study_comments")

            with ui.row():
                ui.button("Save", on_click=self.save)
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")

    async def show(self):
        return await self.dialog
