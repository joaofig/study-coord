from nicegui import ui
from nicemvvm.tools.excel import export_to_excel
from nicemvvm.tools.user import get_user_name, is_user_readonly
from src.viewmodels import ResearcherViewModel
from nicemvvm.viewmodels.view_model import ViewModel
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.researcher_dialog import ResearcherDialog
from src.views.researcher_grid import ResearcherGrid
from nicemvvm.views.view import View


class ResearcherView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with (
                    ui.button(icon="add", on_click=self._show_dialog)
                    .classes("text-xs")
                    .props("padding=xs")
                    .set_enabled(not is_user_readonly())
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
                    .set_enabled(not is_user_readonly())
                ):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                ResearcherGrid(vm)

    async def _on_delete_researcher(self):
        if not is_user_readonly():
            dialog = DeleteWarningDialog(
                "Are you sure you want to delete this researcher?"
            )
            result = await dialog.show()
            if result == "delete":
                dialog.close()
                researcher_id = self.vm.get("selected_id")
                await self.vm.call("delete", researcher_id=researcher_id)
        else:
            ui.notification(
                "You do not have permission to delete researchers.", type="negative"
            )

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
