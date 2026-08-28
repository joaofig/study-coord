from nicegui import ui
from src.tools.user import is_user_readonly
from src.viewmodels.view_model import ViewModel
from src.views.view import View


def validate_number(value: str) -> str | None:
    if not value:
        return "Number is required"
    return None


class ResearcherDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.number = None
        self.name = None

        with ui.dialog() as dialog, ui.card().classes("w-120"):
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("Researcher Details").classes("text-base")

            self.number = (
                ui.input(
                    label="Number",
                    validation=validate_number,
                )
                .classes("w-full")
                .props("dense")
                .bind_value(self.vm, "number")
            )
            self.name = (
                ui.input(label="Name")
                .classes("w-full")
                .props("dense")
                .bind_value(self.vm, "name")
            )

            ui.input(label="Phone").classes("w-full").props("dense").bind_value(
                self.vm, "phone"
            )
            ui.input(label="Email").classes("w-full").props("dense").bind_value(
                self.vm, "email"
            )
            ui.textarea(label="Comments").classes("w-full").props("dense").bind_value(
                self.vm, "comments"
            )

            ui.markdown().classes("bg-orange-200 w-full").bind_content_from(
                self.vm, "validation"
            ).bind_visibility_from(self.vm, "is_invalid")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save()).props(
                    "no-caps"
                ).set_enabled(not is_user_readonly())
                ui.button("Cancel", on_click=lambda: dialog.submit("cancel")).props(
                    "no-caps"
                )
            self.dialog = dialog

    async def save(self):
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")

    async def show(self):
        return await self.dialog
