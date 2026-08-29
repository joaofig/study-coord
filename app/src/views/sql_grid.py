from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


class SQLGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.result = self.vm.get("result")
        if isinstance(self.result, ObservableList):
            self.result.on_change(self._update_grid)
        self.grid: AgGrid = self._build_grid()

    async def _update_grid(self):
        if len(self.result) > 0:
            schema = self.vm.get("schema")
            columns = [
                {"headerName": column[0], "field": column[0]} for column in schema
            ]
            await self.grid.run_grid_method("setGridOption", "columnDefs", columns)
            await self.grid.run_grid_method("setGridOption", "rowData", self.result)

    def _build_grid(self) -> AgGrid:
        grid_def = {
            "columnDefs": [],
            # "autoGenerateColumnDefs": True,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
        }
        return ui.aggrid(options=grid_def, theme="balham").classes("w-full h-full")
