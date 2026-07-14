from nicegui import ui

from src.viewmodels.ViewModel import ViewModel
from src.views.View import View


def validate_required(value: str) -> str | None:
    if not value:
        return "Field is required"
    return None


class EventDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-240"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Event Details").classes("text-base")

            with ui.row().classes("w-full"):
                with ui.column().classes("flex-1"):
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

                with ui.column().classes("flex-1"):
                    ui.date_input(label="Date").bind_value(self.vm, "date") \
                        .classes("w-full")

                    ui.input(label="Event Type", validation=validate_required) \
                        .bind_value(self.vm, "event_type") \
                        .classes("w-full")

                    ui.input(label="Description", validation=validate_required) \
                        .bind_value(self.vm, "description") \
                        .classes("w-full")

                    ui.textarea(label="Comments").bind_value(self.vm, "comments") \
                        .classes("w-full")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save())
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    async def show(self):
        return await self.dialog

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")
