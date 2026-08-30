from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


class ResearcherStudyGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        self.studies = self.vm.get("studies")
        if isinstance(self.studies, ObservableList):
            self.studies.on_change(self._update_grid)
        self.grid = self._build_grid()

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "ID",
                "field": "study_id",
                "hide": True,
            },
            {
                "headerName": "Protocol",
                "field": "protocol",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
                "width": 200,
                "cellStyle": {"fontWeight": "bold"},
            },
            {
                "headerName": "Name",
                "field": "name",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
                "width": 200,
            },
            {
                "headerName": "Sponsor",
                "field": "sponsor",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
                "width": 200,
            },
            {
                "headerName": "Start",
                "field": "start_date",
                "sortable": True,
                "align": "left",
                "width": 90,
            },
            {
                "headerName": "End",
                "field": "end_date",
                "sortable": True,
                "align": "left",
                "width": 90,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.studies,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            # ":getRowId": "(params) => String(params.data.researcher_id)",
        }
        # ui.on("researcher-row-edit", self._on_edit)

        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        # grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _update_grid(self):
        await self.grid.run_grid_method("setGridOption", "rowData", self.studies)
        # print(f"{self.researchers}")
        # Restore the selected researcher
        researcher_id = self.vm.get("researcher_id")
        if researcher_id != 0:
            await self.grid.run_row_method(researcher_id, "setSelected", True)
