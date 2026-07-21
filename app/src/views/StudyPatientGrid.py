from nicegui import ui, app
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from src.viewmodels import PatientViewModel
from src.viewmodels.view_model import ViewModel
from src.views.View import View
from src.views.dialogs.study_patient_dialog import StudyPatientDialog


class StudyPatientGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: AgGrid = self._build_grid()
        self.subscribe("patient", "saved", self._on_patient_saved)

        self.patients = self.vm.get("patients")
        if isinstance(self.patients, ObservableList):
            self.patients.on_change(self._update_grid)

    async def _on_patient_saved(self, **kwargs):
        await self.vm.call("load")
        self._update_grid()

    def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("patients")
        self.grid.update()

    async def _handle_notification(self, action: str, **kwargs):
        if action == "patients_loaded":
            self._update_grid()

    def _build_grid(self) -> AgGrid:
        columns = [
            # {"headerName": "ID", "field": "id", "hide": True},
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
                        emitEvent('patient-row-edit', params.data);
                    });
                return btn;
                }
                """
            },
            {"headerName": "Number", "field": "number", "sortable": True, "align": "left", "width": 100},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left", "width": 120},
            {"headerName": "End", "field": "exit_date", "sortable": True, "align": "left", "width": 120},
            {"headerName": "Status", "field": "status_text", "sortable": True, "align": "left"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        ui.on("patient-row-edit", self._handle_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _edit_patient(self, patient: dict) -> dict:
        vm = PatientViewModel()
        vm.updated_by = app.storage.user.load("username", "Unknown")
        dlg = StudyPatientDialog(vm=vm)
        vm.from_dict(patient)
        result = await dlg.show()
        if result == "save":
            patient = vm.to_dict()
            await self._on_patient_saved()
        return patient

    async def _handle_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            await self._edit_patient(row_data)

    def show(self) -> AgGrid:
        return self.grid

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a study has been selected
            await self.vm.call("patient_selected", patient=row, patient_id=row["id"])
