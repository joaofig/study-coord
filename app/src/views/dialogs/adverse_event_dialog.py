from nicegui import ui
from src.viewmodels.view_model import ViewModel
from src.views.view import View


def validate_required(value: str) -> str | None:
    if not value:
        return "Field is required"
    return None


class AdverseEventDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-240"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Adverse Event Details").classes("text-base")

            with ui.row().classes("w-full"):
                with ui.column().classes("flex-1"):
                    self.select = (
                        ui.select(options=self.vm.get("patients"), label="Patient")
                        .bind_value(self.vm, "patient_id")
                        .on_value_change(
                            lambda: self.vm.call(
                                msg="load_patient", patient_id=self.vm.get("patient_id")
                            )
                        )
                        .classes("w-full")
                    )

                    selection = self.vm.get("selection")
                    ui.input(label="Patient Number") \
                        .props("readonly dense") \
                        .bind_value(selection, "number") \
                        .classes("w-full")

                    ui.input(label="Start Date") \
                        .props("readonly dense") \
                        .bind_value(selection, "start_date") \
                        .classes("w-full") \
                        .props("dense")

                    ui.input(label="Status") \
                        .props("readonly dense") \
                        .bind_value(selection, "status_text") \
                        .classes("w-full") \
                        .props("dense")

                with ui.column().classes("flex-1"):
                    ui.date_input(label="Date")\
                        .bind_value(self.vm, "event_date") \
                        .classes("w-full") \
                        .props("dense")

                    ui.input(label="Event Type", validation=validate_required) \
                        .bind_value(self.vm, "event_type") \
                        .classes("w-full") \
                        .props("dense")

                    ui.input(label="Description", validation=validate_required) \
                        .bind_value(self.vm, "description") \
                        .classes("w-full") \
                        .props("dense")

                    ui.textarea(label="Comments").bind_value(self.vm, "comments") \
                        .classes("w-full") \
                        .props("dense")

            ui.markdown().classes("bg-orange-200 w-full") \
                .bind_content_from(self.vm, "validation") \
                .bind_visibility_from(self.vm, "is_invalid")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save()).props("no-caps")
                ui.button("Close", on_click=lambda: dialog.submit("close")).props("no-caps")
            self.dialog = dialog

    async def show(self):
        return await self.dialog

    async def save(self):
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")
