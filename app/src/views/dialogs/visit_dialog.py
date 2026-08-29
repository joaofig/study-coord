from nicegui import ui
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


def validate_type(value: str) -> str | None:
    if not value:
        return "Visit type is required"
    return None


class StudyVisitDialog(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.dialog() as dialog, ui.card().classes("w-240"):
            with ui.row().classes("w-full  bg-gray-200 p-2"):
                ui.label("Study Visit Details").classes("text-base")

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
                        .props("dense")
                    )

                    selection = self.vm.get("selection")
                    ui.input(label="Patient Number").props("readonly").bind_value(
                        selection, "number"
                    ).classes("w-full").props("dense")

                    ui.input(label="Start Date").props("readonly").bind_value(
                        selection, "start_date"
                    ).classes("w-full").props("dense")

                    ui.input(label="Status").props("readonly").bind_value(
                        selection, "status_text"
                    ).classes("w-full").props("dense")

                with ui.column().classes("flex-1"):
                    ui.date_input(label="Visit Date").bind_value(
                        self.vm, "visit_date"
                    ).classes("w-full").props("dense")

                    ui.input(label="Visit Type", validation=validate_type).bind_value(
                        self.vm, "visit_type"
                    ).classes("w-full").props("dense")

                    ui.textarea(label="Comments").bind_value(
                        self.vm, "comments"
                    ).classes("w-full").props("dense")

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
            self.dialog = dialog

    async def show(self):
        await self.dialog

    async def save(self):
        await self.vm.call("validate")
        is_invalid = self.vm.get("is_invalid")
        if not is_invalid:
            await self.vm.call("save")
            self.dialog.submit("save")
