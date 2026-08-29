import asyncio

from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels.view_model import ViewModel
from src.viewmodels.visit import VisitViewModel
from src.views.dialogs.visit_dialog import StudyVisitDialog
from nicemvvm.views.view import View


class StudyVisitGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        self.visits = self.vm.get("visits")
        if isinstance(self.visits, ObservableList):
            self.visits.on_change(self._update_grid)
        self.subscribe("visit", "saved", self._update_grid)

        self.grid: AgGrid = self._build_grid()

    async def _edit_visit(self, visit_id: int):
        visit_vm = VisitViewModel()
        visit_vm.updated_by = app.storage.user.get("username", "Unknown")
        study_id = self.vm.get("study_id")
        await visit_vm.call("load_patients", study_id=study_id)
        await visit_vm.call("load", visit_id=visit_id)
        dialog = StudyVisitDialog(visit_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=study_id)
            await self.broadcast("study_list", "load")

    async def _on_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            await self._edit_visit(row_data["visit_id"])

    async def _update_grid(self):
        if len(self.visits) > 0:
            await self.grid.run_grid_method("setGridOption", "rowData", self.visits)
        else:
            await self.grid.run_grid_method("setGridOption", "rowData", [])

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "visit_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('visit-row-edit', params.data);
                    });
                return btn;
                }
                """,
            },
            {
                "headerName": "Date",
                "field": "visit_date",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
            {
                "headerName": "Type",
                "field": "visit_type",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter",
                "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_visits_from_database()
            "rowData": self.visits,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.visit_id)",
        }
        ui.on("visit-row-edit", self._on_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on(
            "selectionChanged",
            lambda event: asyncio.create_task(self._row_selection_changed(event)),
        )
        return grid

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify the ViewModel that a visit has been selected
            await self.vm.call("visit_selected", visit_id=row["visit_id"])
        else:
            await self.vm.call("visit_unselected")

    def show(self) -> AgGrid:
        return self.grid
