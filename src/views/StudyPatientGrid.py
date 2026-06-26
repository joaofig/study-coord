from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from tools.messenger import MessengerHub, get_messenger
from viewmodels.ViewModel import ViewModel
from views.View import View


class StudyPatientGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.vm = vm
        self.grid: AgGrid = self._build_grid()
        self.messenger = get_messenger("patient")
        self.messenger.subscribe("saved", self._on_patient_saved)

    async def _on_patient_saved(self, **kwargs):
        await self.command("load_patients")
        self._update_grid()

    def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("patients")
        self.grid.update()

    def _build_grid(self) -> AgGrid:
        columns = [
            {"headerName": "ID", "field": "id", "hide": True},
            {"headerName": "Number", "field": "number", "sortable": True, "align": "left"},
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left"},
            {"headerName": "End", "field": "end_date", "sortable": True, "align": "left"},
            {"headerName": "Status", "field": "status", "sortable": True, "align": "left"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            ":getRowId": "(params) => String(params.data.id)"
        }
        grid = ui.aggrid(grid_def).classes("w-full h-full")
        return grid

    def show(self) -> AgGrid:
        return self.grid
