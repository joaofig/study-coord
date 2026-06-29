from typing import Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from viewmodels.ViewModel import ViewModel


class StudyResearcherGrid:
    def __init__(self, vm: ViewModel):
        self.vm = vm
        self.grid: Any = None

    def show(self) -> AgGrid:
        columns = [
            {"headerName": "ID", "field": "id", "hide": True},
            {"headerName": "Number", "field": "number", "sortable": True, "align": "left"},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Role", "field": "role", "sortable": True, "align": "left"},
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
