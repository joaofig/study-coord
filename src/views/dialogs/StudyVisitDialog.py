from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.View import View


def validate_type(value: str) -> str | None:
    if not value:
        return "Visit type is required"
    return None


class StudyVisitDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-100"):
            ui.label("Study Visit Details").classes("text-base")

            self.select = ui.select(options=self.vm.get("patients"), label="Patient") \
                .bind_value(self.vm, "patient_id") \
                .on_value_change(lambda: self.vm.call(msg="load_patient", patient_id=self.vm.get("patient_id"))) \
                .classes("w-full")

            selection = self.vm.get("selection")
            ui.input(label="Patient Number").props("readonly") \
                .bind_value(selection, "number") \
                .classes("w-full")

            ui.input(label="Start Date").props("readonly") \
                .bind_value(selection, "start_date") \
                .classes("w-full")

            ui.input(label="Status").props("readonly") \
                .bind_value(selection, "status_text") \
                .classes("w-full")

            ui.date_input(label="Visit Date").bind_value(self.vm, "visit_date") \
                .classes("w-full")

            ui.input(label="Visit Type", validation=validate_type) \
                .bind_value(self.vm, "visit_type") \
                .classes("w-full")

            ui.textarea(label="Comments").bind_value(self.vm, "comments") \
                .classes("w-full")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save())
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    async def show(self):
        await self.dialog

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")