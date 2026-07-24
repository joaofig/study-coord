from nicegui import ui

from src.viewmodels.view_model import ViewModel
from src.views.View import View


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    if len(value) < 3:
        return "Name must be at least 3 characters long"
    if len(value) > 128:
        return "Name must be at most 128 characters long"
    return None


def validate_sponsor(value: str | None) -> str | None:
    if not value:
        return "Sponsor name is required"
    if len(value) < 3:
        return "Sponsor name must be at least 3 characters long"
    if len(value) > 128:
        return "Sponsor name must be at most 128 characters long"
    return None


class StudyDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card():
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Details").classes("text-base")

            ui.input(
                label="Name",
                validation=validate_name,
                on_change=lambda: self.vm.call("mark_changed", field_name="name"),
            ).classes("w-full").bind_value(self.vm, "name")

            ui.input(
                label="Sponsor",
                validation=validate_sponsor,
                on_change=lambda: self.vm.call("mark_changed", field_name="sponsor"),
            ).classes("w-full").bind_value(self.vm, "sponsor")

            with ui.row().classes("gap-2"):
                ui.date_input(
                    label="Start Date",
                    on_change=lambda: self.vm.call(
                        "mark_changed", field_name="start_date"
                    ),
                ).bind_value(self.vm, "start_date")
                ui.date_input(
                    label="End Date",
                    on_change=lambda: self.vm.call(
                        "mark_changed", field_name="end_date"
                    ),
                ).bind_value(self.vm, "end_date")

            with ui.row().classes("gap-2"):
                ui.number(
                    label="Protocol Visits",
                    value=1, min=1, step=1,
                    on_change=lambda: self.vm.call(
                        "mark_changed", field_name="protocol_visits"
                    ),
                ).props("clearable").classes("w-full").bind_value(
                    self.vm, "protocol_visits", strict=True
                )

            with ui.row().classes("gap-2 w-full"):
                ui.textarea(
                    label="Comments",
                    on_change=lambda: self.vm.call(
                        "mark_changed", field_name="comments"
                    ),
                ).classes("w-full").bind_value(self.vm, "comments")

            with ui.row():
                ui.button("Save", on_click=self.save)
                ui.button("Close", on_click=lambda: dialog.submit("close"))
            self.dialog = dialog

    async def show(self):
        await self.dialog

    async def save(self):
        await self.vm.call("save")
        self.dialog.submit("save")
