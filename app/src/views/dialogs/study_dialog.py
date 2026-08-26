from nicegui import ui

from src.tools.user import is_user_readonly
from src.viewmodels.view_model import ViewModel
from src.views.view import View


def validate_name(value: str | None) -> str | None:
    if not value:
        return "Name is required"
    if len(value) < 3:
        return "Name must be at least 3 characters long"
    return None


def validate_sponsor(value: str | None) -> str | None:
    if not value:
        return "Sponsor name is required"
    if len(value) < 3:
        return "Sponsor name must be at least 3 characters long"
    if len(value) > 128:
        return "Sponsor name must be at most 128 characters long"
    return None


def validate_protocol(value: str | None) -> str | None:
    if not value:
        return "Sponsor name is required"
    if len(value) < 3:
        return "Sponsor name must be at least 3 characters long"
    if len(value) > 64:
        return "Sponsor name must be at most 128 characters long"
    return None


class StudyDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-240"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Details").classes("text-base")

            ui.input(label="Protocol", validation=validate_protocol) \
                .classes("w-full") \
                .bind_value(self.vm, "protocol") \
                .props("dense")

            ui.input(
                label="Name",
                validation=validate_name,
            ).classes("w-full").bind_value(self.vm, "name").props("dense")

            ui.input(
                label="Sponsor",
                validation=validate_sponsor,
            ).classes("w-full").bind_value(self.vm, "sponsor").props("dense")

            with ui.row():
                self.start_date = ui.date_input(label="Start Date") \
                    .bind_value(self.vm, "start_date") \
                    .classes("w-36").props("dense")

                self.end_date = ui.date_input(label="End Date") \
                    .bind_value(self.vm, "end_date")\
                    .classes("w-40") \
                    .props("clearable dense")

                ui.number(label="Protocol Visits", value=1, min=1, step=1,) \
                    .props("clearable dense") \
                    .bind_value(self.vm, "protocol_visits", strict=True) \
                    .classes("w-36")

            with ui.row().classes("gap-2 w-full"):
                ui.textarea(label="Comments") \
                    .classes("w-full") \
                    .props("dense") \
                    .bind_value(self.vm, "comments")

            ui.markdown().classes("bg-orange-200 w-full") \
                .bind_content_from(self.vm, "validation") \
                .bind_visibility_from(self.vm, "is_invalid")

            with ui.row():
                ui.button("Save", on_click=self.save) \
                    .props("no-caps") \
                    .set_enabled(not is_user_readonly())
                ui.button("Close", on_click=lambda: dialog.submit("close")).props("no-caps")
            self.dialog = dialog

    async def show(self):
        await self.dialog

    async def save(self):
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")
