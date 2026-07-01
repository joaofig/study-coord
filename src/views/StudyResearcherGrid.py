from typing import Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from viewmodels.ViewModel import ViewModel
from views.View import View


class StudyResearcherGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: Any = None

    def _update_grid(self):
        researchers = self.vm.get("researchers")
        print(researchers)
        self.grid.options["rowData"] = researchers
        self.grid.update()

    def show(self) -> AgGrid:
        columns = [
            {"headerName": "ID", "field": "id", "hide": True},
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
        self.grid = ui.aggrid(grid_def).classes("w-full h-full")
        return self.grid

    def _handle_notification(self, action: str, **kwargs):
        match action:
            case "study_researchers_loaded":
                self._update_grid()
