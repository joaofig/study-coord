from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels.monitorization import MonitorizationViewModel
from src.viewmodels.view_model import ViewModel
from src.views.dialogs.monitorization_dialog import StudyMonitorizationDialog
from src.views.view import View


class StudyMonitorizationGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        self.monitorization_visits = self.vm.get("monitorization_visits")
        if isinstance(self.monitorization_visits, ObservableList):
            self.monitorization_visits.on_change(self._update_grid)

        self.grid: AgGrid = self._build_grid()

    async def _update_grid(self):
        await self.grid.run_grid_method(
            "setGridOption", "rowData", self.monitorization_visits
        )

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "monitoring_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('monitoring-row-edit', params.data);
                    });
                return btn;
                }
                """,
            },
            {
                "headerName": "Date",
                "field": "meeting_date",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Monitor",
                "field": "monitor",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Comments",
                "field": "comments",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.monitorization_visits,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.monitoring_id)",
        }
        ui.on("monitoring-row-edit", self._handle_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _edit_monitoring(self, monitoring: dict) -> dict:
        vm = MonitorizationViewModel()
        vm.updated_by = app.storage.user.get("username", "Unknown")
        dlg = StudyMonitorizationDialog(vm=vm)
        vm.from_dict(monitoring)
        result = await dlg.show()
        if result == "save":
            monitoring = vm.to_dict()
            await self.vm.call("load")
        return monitoring

    async def _handle_edit(self, event):
        row_data = event.args
        if row_data:
            await self._edit_monitoring(row_data)

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call(
                "select", monitoring=row, monitoring_id=row["monitoring_id"]
            )
