from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels import StudyViewModel
from src.viewmodels.view_model import ViewModel
from src.views.dialogs.study_dialog import StudyDialog
from src.views.view import View


class StudyGrid(View):
    def __init__(self, vm: ViewModel) -> None:
        super().__init__(vm)
        self.studies = self.vm.get("studies")
        if isinstance(self.studies, ObservableList):
            self.studies.on_change(self._update_grid)
        self.grid = self._build_grid()

    async def _update_grid(self):
        await self.grid.run_grid_method("setGridOption", "rowData", self.studies)

        # Restore the selected study
        study_id = self.vm.get("selected_id")
        if study_id != 0:
            await self.grid.run_row_method(study_id, "setSelected", True)

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a study has been selected
            await self.vm.call("select", study_id=row["study_id"])

    async def _on_edit(self, event):
        # Handle the edit button click event from the AgGrid component
        row = event.args
        if row:
            vm = StudyViewModel()
            dialog = StudyDialog(vm)
            await vm.call("load", study_id=row["study_id"])
            result = await dialog.show()
            if result == "save":
                await self.vm.call("load")  # Reload the grid after saving

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "study_id",
                "width": 50,
                ":cellRenderer": """
            (params) => {
                const btn = document.createElement('button');
                btn.innerText = '✏️';
                btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                btn.addEventListener('click', () => {
                    emitEvent('study-row-edit', params.data);
                });
                return btn;
            }
            """,
            },
            {
                "headerName": "Protocol", "field": "protocol", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False, "width": 200,
                "cellStyle": {"fontWeight": "bold"},
            },
            {
                "headerName": "Name", "field": "name", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False, "width": 200,
            },
            {
                "headerName": "Sponsor", "field": "sponsor", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False, "width": 200,
            },
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left", "width": 90,},
            {"headerName": "End", "field": "end_date", "sortable": True, "align": "left", "width": 90,},
            {"headerName": "Patients", "field": "patients", "sortable": True, "type": "numericColumn", "width": 90,},
            {"headerName": "Visits", "field": "visits", "sortable": True, "type": "numericColumn", "width": 90,},
            {"headerName": "Researchers", "field": "researchers", "sortable": True, "type": "numericColumn", "width": 90,},
            {"headerName": "Adverse Events", "field": "events", "sortable": True, "type": "numericColumn", "width": 90,},
            # {"headerName": "Monitorizations", "field": "monitorizations", "sortable": True, "type": "numericColumn", "width": 90,},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": self.studies,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.study_id)",
        }
        ui.on("study-row-edit", self._on_edit)
        self.grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        self.grid.on("selectionChanged",
                     lambda event: self._row_selection_changed(event)
                     )
        return self.grid
