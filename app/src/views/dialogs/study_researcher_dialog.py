from nicegui import ui
from nicegui.elements.dialog import Dialog
from src.viewmodels.view_model import ViewModel
from src.views.view import View


def validate_researcher_number(value: str | None) -> str | None:
    if not value:
        return "Researcher Number is required"
    return None


class StudyResearcherDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.dialog: Dialog = self._build_dialog()

    async def save(self):
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")

    async def show(self):
        return await self.dialog

    def _build_dialog(self) -> Dialog:
        with ui.dialog() as dialog, ui.card().classes("w-120"):
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("Study Researcher Details").classes("text-base")

            ui.select(
                options=self.vm.get("researchers"),
                label="Researcher Number",
                validation=validate_researcher_number,
            ).bind_value(self.vm, "researcher_id").on_value_change(
                lambda: self.vm.call("load")
            ).classes("w-full").props("dense")

            selection = self.vm.get("selection")
            ui.input(label="Name").props("readonly dense").classes("w-full").bind_value(
                selection, "name"
            )

            ui.input(label="Phone").props("readonly dense").classes(
                "w-full"
            ).bind_value(selection, "phone")
            ui.input(label="Email").props("readonly dense").classes(
                "w-full"
            ).bind_value(selection, "email")

            ui.select(options=self.vm.get("roles"), label="Role").bind_value(
                self.vm, "role"
            ).classes("w-full").props("dense")

            ui.textarea(label="Study Comments").classes("w-full").props(
                "dense"
            ).bind_value(self.vm, "study_comments")

            ui.markdown().classes("bg-orange-200 w-full").bind_content_from(
                self.vm, "validation"
            ).bind_visibility_from(self.vm, "is_invalid")

            with ui.row():
                ui.button("Save", on_click=lambda: self.save()).props(
                    "no-caps"
                ).set_enabled(not is_user_readonly())
                ui.button("Close", on_click=lambda: dialog.submit("close")).props(
                    "no-caps"
                )
        return dialog
