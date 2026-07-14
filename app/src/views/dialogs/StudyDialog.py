from nicegui import ui

from src.viewmodels.ViewModel import ViewModel
from src.views.View import View


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    return None


class StudyDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card():
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Details").classes("text-base")

            ui.input(label="Name", validation=validate_name,
                     on_change=lambda: self.vm.call("mark_changed", field_name="name")) \
                .classes("w-full") \
                .bind_value(self.vm, "name")

            ui.input(label="Sponsor",
                     on_change=lambda: self.vm.call("mark_changed", field_name="sponsor")) \
                .classes("w-full") \
                .bind_value(self.vm, "sponsor")

            with ui.row().classes("gap-2"):
                ui.date_input(label="Start Date",
                              on_change=lambda: self.vm.call("mark_changed", field_name="start_date")) \
                    .bind_value(self.vm, "start_date")
                ui.date_input(label="End Date",
                              on_change=lambda: self.vm.call("mark_changed", field_name="end_date")) \
                    .bind_value(self.vm, "end_date")

            with ui.row().classes("gap-2"):
                ui.number(label="Protocol Visits", value=1,
                          on_change=lambda: self.vm.call("mark_changed", field_name="visits")) \
                    .props('clearable') \
                    .classes("w-full") \
                    .bind_value(self.vm, "visits", strict=True)

            with ui.row().classes("gap-2 w-full"):
                ui.textarea(label="Comments",
                            on_change=lambda: self.vm.call("mark_changed", field_name="comments")) \
                    .classes("w-full") \
                    .bind_value(self.vm, "comments")

            with ui.row():
                ui.button("Save", on_click=self.save)
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    async def show(self):
        await self.dialog

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")
