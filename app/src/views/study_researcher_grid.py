
from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels.study_researcher import StudyResearcherViewModel
from src.viewmodels.view_model import ViewModel
from src.views.dialogs.study_researcher_dialog import StudyResearcherDialog
from src.views.view import View


class StudyResearcherGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: AgGrid = self._build_grid()
        self.researchers = self.vm.get("researchers")
        if isinstance(self.researchers, ObservableList):
            self.researchers.on_change(self._update_grid)

        self.subscribe(
            channel="study_researcher", message="saved", handler=self._refresh_grid
        )
        self.subscribe(
            channel="study_researcher", message="deleted", handler=self._refresh_grid
        )
        self.subscribe(channel="patient", message="saved", handler=self._refresh_grid)
        self.subscribe(channel="study", message="selected", handler=self._refresh_grid)

    async def _refresh_grid(self, **kwargs):
        await self.vm.call("load")

    async def _update_grid(self):
        await self.grid.run_grid_method("setGridOption", "rowData", self.researchers)

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "sr_id",
                "width": 50,
                ":cellRenderer": """
            (params) => {
                const btn = document.createElement('button');
                btn.innerText = '✏️';
                btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                btn.addEventListener('click', () => {
                    emitEvent('study-researcher-row-edit', params.data);
                });
                return btn;
            }
            """,
            },
            {
                "headerName": "Number",
                "field": "number",
                "sortable": True,
                "align": "left",
                "width": 100,
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Name", "field": "name", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
             },
            {
                "headerName": "Role",
                "field": "role_text",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Phone",
                "field": "phone",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Email",
                "field": "email",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.sr_id)",
        }
        ui.on("study-researcher-row-edit", self._on_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on(
            "selectionChanged", lambda event: self._row_selection_changed(event)
        )
        return grid

    def show(self) -> AgGrid:
        return self.grid

    async def _edit_researcher(self, researcher: dict) -> dict:
        researcher_vm = StudyResearcherViewModel()
        researcher_vm.updated_by = app.storage.user.get("username", "Unknown")
        await researcher_vm.load_researchers()
        researcher_vm.from_dict(researcher)

        dialog = StudyResearcherDialog(vm=researcher_vm)
        result = await dialog.show()
        if result == "save":
            researcher = researcher_vm.to_dict()
            await self._refresh_grid()
        return researcher

    async def _on_edit(self, event):
        row_data = event.args  # dict with the full row's data
        print(row_data)
        if row_data:
            await self._edit_researcher(row_data)

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a study has been selected
            await self.vm.call("researcher_selected", researcher_id=row["sr_id"])
        else:
            await self.vm.call("researcher_unselected")
