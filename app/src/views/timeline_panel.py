from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View


class TimelinePanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        self.milestones = self.vm.get("milestones")
        if isinstance(self.milestones, ObservableList):
            self.milestones.on_change(self._update_grid)

        self.grid: AgGrid = self._build_grid()

    async def _update_grid(self):
        await self.grid.run_grid_method("setGridOption", "rowData", self.milestones)

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Date",
                "field": "event_date",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Event",
                "field": "event_title",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Description",
                "field": "description",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.milestones,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            # ":getRowId": "(params) => String(params.data.selected_id)",
        }
        # ui.on("event-row-edit", self._on_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        # grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid
