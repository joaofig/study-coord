from nicegui import ui
from nicemvvm.tools.excel import export_to_excel
from nicemvvm.tools.user import is_user_readonly
from src.viewmodels import StudyViewModel
from nicemvvm.viewmodels.view_model import ViewModel
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.study_dialog import StudyDialog
from src.views.study_grid import StudyGrid
from src.views.study_panel import StudyPanel
from nicemvvm.views.view import View


async def _new_study_dialog():
    study_vm = StudyViewModel()
    dialog = StudyDialog(study_vm)
    await dialog.show()


class StudyView(View):
    """
    This is the main Study view, which contains the StudyGrid and StudyEditor components.
    It is responsible for managing the layout and interactions between these components.
    """

    def __init__(self, vm: ViewModel):
        super().__init__(vm)

    async def _on_delete_study(self):
        if not is_user_readonly():
            dialog = DeleteWarningDialog("Are you sure you want to delete this study?")
            result = await dialog.show()
            if result == "delete":
                dialog.close()
                study_id = self.vm.get("selected_id")
                await self.vm.call("delete", study_id=study_id)
        else:
            ui.notification(
                "You do not have permission to delete studies.", type="negative"
            )

    def show(self):
        with ui.splitter(horizontal=True, value=35).classes(
            "w-full h-full"
        ) as splitter:
            with splitter.before, ui.row().classes("w-full h-full"):
                with ui.column().classes("h-full flex-none pl-0"):
                    with (
                        ui.button(icon="add", on_click=_new_study_dialog)
                        .classes("text-xs")
                        .set_enabled(not is_user_readonly())
                        .props("padding=xs")
                    ):
                        ui.tooltip("Add Study")
                    with (
                        ui.button(
                            icon="delete", on_click=lambda: self._on_delete_study()
                        )
                        .bind_enabled(self.vm, "selected_id")
                        .classes("text-xs")
                        .props("color=red padding=xs")
                    ):
                        ui.tooltip("Delete Study")
                    with (
                        ui.button(
                            icon="table_view",
                            on_click=lambda: self._on_export_to_excel(),
                        )
                        .classes("text-xs")
                        .set_enabled(not is_user_readonly())
                        .props("padding=xs")
                    ):
                        ui.tooltip("Export to Excel")

                with ui.column().classes("h-full flex-1"):
                    StudyGrid(self.vm)

            with splitter.after:
                StudyPanel(self.vm)

    def _on_export_to_excel(self):
        studies = self.vm.get("studies")
        if studies:
            export_to_excel(studies, filename="studies.xlsx")
