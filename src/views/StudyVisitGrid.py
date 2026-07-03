from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from viewmodels.ViewModel import ViewModel
from views.View import View


class StudyVisitGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: AgGrid = self._build_grid()
        self.visits = self.vm.get("visits")
        if isinstance(self.visits, ObservableList):
            self.visits.on_change(self._update_grid)
        self.subscribe("visit", "saved", self._update_grid)

    def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("visits")
        self.grid.update()

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "id",
                "width": 80,
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
            {"headerName": "Date", "field": "date", "sortable": True, "align": "left", "width": 120},
            {"headerName": "Type", "field": "type", "sortable": True, "align": "left"},
            {"headerName": "Status", "field": "status_text", "sortable": True, "align": "left"},
            {"headerName": "Patient", "field": "patient_number", "sortable": True, "align": "left"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_visits_from_database()
            "rowData": [],
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        # ui.on("visit-row-edit", self._handle_edit)
        grid = ui.aggrid(grid_def).classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify the ViewModel that a visit has been selected
            await self.vm_message("visit_selected", visit_id=row["id"])
        else:
            await self.vm_message("visit_unselected")

    def show(self) -> AgGrid:
        return self.grid