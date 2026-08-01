from nicegui import ui

from src.tools.excel import export_to_excel
from src.viewmodels import ResearcherViewModel
from src.viewmodels.view_model import ViewModel
from src.views.researcher_grid import ResearcherGrid
from src.views.view import View
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.researcher_dialog import ResearcherDialog
from src.tools.user import logout, get_user_name


class ResearcherView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with (
                    ui.button(icon="add", on_click=self._show_dialog)
                    .classes("text-xs")
                    .props("padding=xs")
                ):
                    ui.tooltip("Add Researcher")

                with (
                    ui.button(icon="delete", on_click=self._on_delete_researcher)
                    .bind_enabled(self.vm, "selected_id")
                    .classes("text-xs")
                    .props("padding=xs color=red")
                ):
                    ui.tooltip("Delete Researcher")

                with (
                    ui.button(icon="table_view", on_click=self._on_export_to_excel)
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
                ResearcherGrid(vm).show()

    async def _on_delete_researcher(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this researcher?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            researcher_id = self.vm.get("selected_id")
            await self.vm.call("delete", researcher_id=researcher_id)

    async def _show_dialog(self):
        vm = ResearcherViewModel()
        vm.created_by = get_user_name()
        dialog = ResearcherDialog(vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    def _on_export_to_excel(self):
        researchers = [r.to_dict() for r in self.vm.get("researchers")]
        if researchers:
            export_to_excel(researchers, filename="researchers.xlsx")
