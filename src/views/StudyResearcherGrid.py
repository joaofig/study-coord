from typing import Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from viewmodels.StudyResearcherViewModel import StudyResearcherViewModel
from viewmodels.ViewModel import ViewModel
from views.View import View
from views.dialogs.StudyResearcherDialog import StudyResearcherDialog


class StudyResearcherGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: Any = None
        self.subscribe(channel="study_researcher",
                       message="saved",
                       handler=self._refresh_grid)
        self.subscribe(channel="patient",
                       message="saved",
                       handler=self._refresh_grid)
        self.subscribe(channel="study",
                       message="study_selected",
                       handler=self._refresh_grid)

    async def _refresh_grid(self, **kwargs):
        await self.vm_message("load")
        self._update_grid()

    def _update_grid(self):
        researchers = self.vm.get("researchers")
        self.grid.options["rowData"] = researchers
        self.grid.update()

    def show(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "id",
                "width": 80,
                ":cellRenderer": """
            (params) => {
                const btn = document.createElement('button');
                btn.innerText = '✏️';
                btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                btn.addEventListener('click', () => {
                    emitEvent('study-researcher-row-edit', params.data);
                });
                return btn;
            }
            """
            },
            {"headerName": "Number", "field": "number", "sortable": True, "align": "left"},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Role", "field": "role_text", "sortable": True, "align": "left"},
            {"headerName": "Phone", "field": "phone", "sortable": True, "align": "left"},
            {"headerName": "Email", "field": "email", "sortable": True, "align": "left"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            ":getRowId": "(params) => String(params.data.id)"
        }
        ui.on("study-researcher-row-edit", self._on_edit)
        self.grid = ui.aggrid(grid_def).classes("w-full h-full")
        return self.grid

    async def _edit_researcher(self, researcher: dict) -> dict:
        researcher_vm = StudyResearcherViewModel()
        await researcher_vm.load_researchers()
        await researcher_vm.message("load", researcher_id=researcher["id"])

        dialog = StudyResearcherDialog(vm=researcher_vm)
        result = await dialog.show()
        if result == "save":
            researcher = researcher_vm.to_dict()
            await self._refresh_grid()
        return researcher

    async def _on_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            await self._edit_researcher(row_data)