import asyncio
from datetime import datetime

from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels import PatientViewModel
from src.viewmodels.view_model import ViewModel
from src.views.dialogs.patient_dialog import StudyPatientDialog
from src.views.view import View


class StudyPatientGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.patients = self.vm.get("patients")
        if isinstance(self.patients, ObservableList):
            self.patients.on_change(self._update_grid)

        self.grid: AgGrid = self._build_grid()
        self.subscribe("patient", "saved", self._on_patient_saved)


    async def _on_patient_saved(self, **kwargs):
        await self.vm.call("load")

    async def _update_grid(self):
        await self.grid.run_grid_method("setGridOption", "rowData", self.patients)

        # Restore the selected patient
        patient_id = self.vm.get("selected_id")
        if patient_id != 0:
            await self.grid.run_row_method(patient_id, "setSelected", True)

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "patient_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('patient-row-edit', params.data);
                    });
                return btn;
                }
                """,
            },
            {
                "headerName": "Number", "field": "number", "sortable": True, "align": "left", "width": 100,
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Name", "field": "name", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Start", "field": "start_date", "sortable": True, "align": "left", "width": 120,
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "End", "field": "exit_date", "sortable": True, "align": "left", "width": 120,
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Status", "field": "status_text", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": self.patients,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.patient_id)",
        }
        ui.on("patient-row-edit", self._handle_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: asyncio.create_task(self._row_selection_changed(event)))
        return grid

    async def _edit_patient(self, patient: dict) -> dict:
        vm = PatientViewModel()
        vm.from_dict(patient)
        vm.updated_by = app.storage.user.get("username", "Unknown")
        vm.updated_at = datetime.now()

        dlg = StudyPatientDialog(vm=vm)

        result = await dlg.show()
        if result == "save":
            patient = vm.to_dict()
            await self._on_patient_saved()
        return patient

    async def _handle_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            await self._edit_patient(row_data)

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a patient has been selected
            await self.vm.call(
                "patient_selected", patient=row, patient_id=row["patient_id"]
            )
