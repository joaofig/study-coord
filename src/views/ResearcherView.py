from nicegui import ui

from tools.excel import export_to_excel
from viewmodels import ResearcherViewModel
from viewmodels.ViewModel import ViewModel
from views.ResearcherGrid import ResearcherGrid
from views.View import View
from views.dialogs.DeleteWarningDialog import DeleteWarningDialog


class ResearcherView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=self._show_dialog) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add Researcher")

                with ui.button(icon="delete") \
                        .bind_enabled(self.vm, "selected_id") \
                        .classes("text-xs") \
                        .props("padding=xs color=red"):
                    ui.tooltip("Delete Researcher")

                with ui.button(icon="table_view", on_click=self._on_export_to_excel) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                self.grid = ResearcherGrid(vm)

    async def _on_delete_researcher(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this researcher?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            researcher_id = self.vm.get("researcher_id")
            await self.vm.call("delete_researcher", researcher_id=researcher_id)
            await self.vm.call("load")
            await self.broadcast("researcher_list", "load")

    async def _show_dialog(self):
        from views.dialogs.ResearcherDialog import ResearcherDialog
        dialog = ResearcherDialog(ResearcherViewModel())
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    def _on_export_to_excel(self):
        researchers = [r.to_dict() for r in self.vm.get("researchers")]
        if researchers:
            export_to_excel(researchers, filename="researchers.xlsx")
