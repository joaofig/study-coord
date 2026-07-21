from nicegui import ui, app
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from src.viewmodels.view_model import ViewModel
from src.viewmodels.visit import VisitViewModel
from src.views.View import View
from src.views.dialogs.study_visit_dialog import StudyVisitDialog


class StudyVisitGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: AgGrid = self._build_grid()
        self.visits = self.vm.get("visits")
        if isinstance(self.visits, ObservableList):
            self.visits.on_change(self._update_grid)
        self.subscribe("visit", "saved", self._update_grid)

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
            await self._edit_visit(row_data["id"])

    async def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("visits")
        self.grid.update()

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "id",
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
                """
            },
            {"headerName": "Date", "field": "visit_date", "sortable": True, "align": "left", "width": 120},
            {"headerName": "Type", "field": "visit_type", "sortable": True, "align": "left"},
            {"headerName": "Patient Number", "field": "patient_number", "sortable": True, "align": "left"},
            {"headerName": "Patient Name", "field": "patient_name", "sortable": True, "align": "left"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_visits_from_database()
            "rowData": [],
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        ui.on("visit-row-edit", self._on_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify the ViewModel that a visit has been selected
            await self.vm.call("visit_selected", visit_id=row["id"])
        else:
            await self.vm.call("visit_unselected")

    def show(self) -> AgGrid:
        return self.grid