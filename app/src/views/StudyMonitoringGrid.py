from nicegui import ui, app
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from src.viewmodels.monitoring import MonitoringViewModel
from src.viewmodels.view_model import ViewModel
from src.views.View import View
from src.views.dialogs.study_monitoring_dialog import StudyMonitoringDialog


class StudyMonitoringGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: AgGrid = self._build_grid()
        self.subscribe("monitoring", "saved", self._on_monitoring_saved)

        self.monitoring_visits = self.vm.get("monitoring_visits")
        if isinstance(self.monitoring_visits, ObservableList):
            self.monitoring_visits.on_change(self._update_grid)

    async def _on_monitoring_saved(self, **kwargs):
        await self.vm.call("load")
        self._update_grid()

    def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("monitoring_visits")
        self.grid.update()

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
            },
            {
                "headerName": "Monitor",
                "field": "monitor",
                "sortable": True,
                "align": "left",
            },
            {
                "headerName": "Comments",
                "field": "comments",
                "sortable": True,
                "align": "left",
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": [],
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.id)",
        }
        ui.on("monitoring-row-edit", self._handle_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _edit_monitoring(self, monitoring: dict) -> dict:
        vm = MonitoringViewModel()
        vm.updated_by = app.storage.user.get("username", "Unknown")
        dlg = StudyMonitoringDialog(vm=vm)
        vm.from_dict(monitoring)
        result = await dlg.show()
        if result == "save":
            monitoring = vm.to_dict()
            await self._on_monitoring_saved()
        return monitoring

    async def _handle_edit(self, event):
        row_data = event.args
        if row_data:
            await self._edit_monitoring(row_data)

    def show(self) -> AgGrid:
        return self.grid

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call(
                "monitoring_selected",
                monitoring=row,
                monitoring_id=row["monitoring_id"],
            )
