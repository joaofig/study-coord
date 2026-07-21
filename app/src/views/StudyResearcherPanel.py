from nicegui import ui

from src.tools.excel import export_to_excel
from src.tools.messenger import get_messenger
from src.viewmodels.study_researcher import StudyResearcherViewModel
from src.viewmodels.view_model import ViewModel
from src.views.StudyResearcherGrid import StudyResearcherGrid
from src.views.View import View
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog
from src.views.dialogs.study_researcher_dialog import StudyResearcherDialog


class StudyResearcherPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.study_id = 0
        self.messenger = get_messenger("study_researcher")
        self.messenger.subscribe("study_researcher_selected", self._study_researcher_selected)

        self.subscribe("study", "selected", self._study_selected)

    async def _study_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _new_researcher_dialog(self):
        researcher_vm = StudyResearcherViewModel()
        await researcher_vm.load_researchers()
        researcher_vm.study_id = self.study_id
        dialog = StudyResearcherDialog(researcher_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")
            await self.broadcast("study_list", "load")

    async def _study_researcher_selected(self, **kwargs):
        if "study_id" in kwargs:
            self.study_id = kwargs["study_id"]

    async def _on_delete_researcher(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this researcher?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            selected_id = self.vm.get("selected_id")
            if selected_id:
                researcher_id = selected_id
                await self.vm.call("delete_researcher", researcher_id=researcher_id)
            await self.broadcast("study_list", "load")

    def show(self):
        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=lambda: self._new_researcher_dialog()) \
                        .props("padding=xs") \
                        .classes("text-xs"):
                    ui.tooltip("Add Researcher")

                with ui.button(icon="delete", on_click=lambda: self._on_delete_researcher()) \
                        .bind_enabled(self.vm, "selected_id") \
                        .props("color=red padding=xs") \
                        .classes("text-xs"):
                    ui.tooltip("Delete Researcher")

                with ui.button(icon="table_view", on_click=self._export_to_excel) \
                        .props("padding=xs") \
                        .classes("text-xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                StudyResearcherGrid(self.vm).show()

    def _export_to_excel(self):
        researchers = [r.to_dict() for r in self.vm.get("researchers")]
        export_to_excel(researchers, "study_researchers.xlsx")