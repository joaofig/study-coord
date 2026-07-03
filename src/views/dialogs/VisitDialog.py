from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.View import View


class VisitDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-100"):
            ui.label("Study Visit Details").classes("text-base")

            self.select = ui.select(options=self.vm.get("patients"), label="Patient") \
                .bind_value(self.vm, "patient_id") \
                .classes("w-full")

            ui.input(label="Patient Number").props("readonly") \
                .classes("w-full")

            ui.input(label="Patient Name").props("readonly") \
                .classes("w-full")

            ui.date_input(label="Visit Date").bind_value(self.vm, "visit_date") \
                .classes("w-full")

            ui.input(label="Visit Type").bind_value(self.vm, "visit_type") \
                .classes("w-full")

            ui.textarea(label="Comments").bind_value(self.vm, "comments") \
                .classes("w-full")

            with ui.row():
                ui.button("Save", on_click=lambda: dialog.submit("save"))
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog
