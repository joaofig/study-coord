from nicegui import ui

from src.tools.user import logout
from src.tools.excel import export_to_excel
from src.viewmodels import StudyViewModel
from src.viewmodels.view_model import ViewModel
from src.views.study_grid import StudyGrid
from src.views.StudyPanel import StudyPanel
from src.views.View import View
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.study_dialog import StudyDialog


class StudyView(View):
    """
    This is the main Study view, which contains the StudyGrid and StudyEditor components.
    It is responsible for managing the layout and interactions between these components.
    """

    def __init__(self, vm: ViewModel):
        super().__init__(vm)

    async def load(self):
        await self.vm.call("load")

    async def _on_delete_study(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this study?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            study_id = self.vm.get("study_id")
            await self.vm.call("delete_study", study_id=study_id)
            await self.vm.call("load")

    async def _new_study_dialog(self):
        study_vm = StudyViewModel()
        dialog = StudyDialog(study_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    def show(self):
        with ui.splitter(horizontal=True).classes("w-full h-full") as splitter:
            with splitter.before:
                with ui.row().classes("w-full h-full"):
                    with ui.column().classes("h-full flex-none pl-0"):
                        with (
                            ui.button(
                                icon="add", on_click=lambda: self._new_study_dialog()
                            )
                            .classes("text-xs")
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
                            .props("padding=xs")
                        ):
                            ui.tooltip("Export to Excel")

                        ui.separator()

                        with (
                            ui.button(icon="logout", on_click=logout)
                            .classes("text-xs")
                            .props("padding=xs")
                        ):
                            ui.tooltip("Log Out")

                    with ui.column().classes("h-full flex-1"):
                        grid = StudyGrid(self.vm)
                        grid.show()

            with splitter.after:
                StudyPanel(self.vm)

    def _on_export_to_excel(self):
        studies = self.vm.get("studies")
        if studies:
            export_to_excel(studies, filename="studies.xlsx")
