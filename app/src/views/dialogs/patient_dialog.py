from nicegui import ui
from nicegui.elements.dialog import Dialog
from src.tools.user import is_user_readonly
from src.viewmodels.view_model import ViewModel
from src.views.view import View


def validate_patient_number(value: str | None) -> str | None:
    if not value:
        return "Patient number is required"
    return None


class StudyPatientDialog(View):
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
        statuses = self.vm.get("statuses")
        with ui.dialog() as dialog, ui.card().classes("w-280"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Patient Details").classes("text-base")

            with ui.row().classes("w-full"):
                with ui.column():
                    ui.input("Number", validation=validate_patient_number).classes(
                        "w-full"
                    ).props("dense").bind_value(self.vm, "number")

                    ui.input("Name").classes("w-full").props("dense").bind_value(
                        self.vm, "name"
                    )

                    with ui.row():
                        ui.date_input("Start Date").classes("w-36").props(
                            "dense"
                        ).bind_value(self.vm, "start_date")
                        ui.date_input("Exit Date").classes("w-36").props(
                            "dense"
                        ).bind_value(self.vm, "exit_date")

                    ui.select(options=statuses, label="Status", value="active").classes(
                        "w-full"
                    ).props("dense").bind_value(self.vm, "status")

                with ui.column().classes("flex-1"):
                    ui.textarea("Comments").classes("w-full h-full").props(
                        "dense"
                    ).bind_value(self.vm, "comments")

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
