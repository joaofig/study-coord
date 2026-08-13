from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels import ResearcherViewModel
from src.viewmodels.view_model import ViewModel
from src.views.view import View


class ResearcherGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        self.researchers = self.vm.get("researchers")
        if isinstance(self.researchers, ObservableList):
            self.researchers.on_change(self._update_grid)
        self.grid = self._build_grid()

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "researcher_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('researcher-row-edit', params.data);
                    });
                return btn;
                }
                """,
            },
            {
                "headerName": "Number", "field": "number", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
                "cellStyle": {"fontWeight": "bold"},
            },
            {
                "headerName": "Name", "field": "name", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Phone", "field": "phone", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Email", "field": "email", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
             },
            {
                "headerName": "Comments", "field": "comments", "sortable": True, "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {"headerName": "Studies", "field": "study_count", "sortable": True, "align": "right",},
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.researchers,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.researcher_id)",
        }
        ui.on("researcher-row-edit", self._on_edit)

        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _on_researcher_saved(self, **kwargs):
        await self.vm.call("load")  # Reload the grid after a researcher is saved

    async def _update_grid(self):
        await self.grid.run_grid_method("setGridOption", "rowData", self.researchers)
        # print(f"{self.researchers}")
        # Restore the selected researcher
        researcher_id = self.vm.get("selected_id")
        if researcher_id != 0:
            await self.grid.run_row_method(researcher_id, "setSelected", True)

    async def _on_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            from src.views.dialogs.researcher_dialog import ResearcherDialog

            vm = ResearcherViewModel()
            vm.updated_by = app.storage.user.get("username", "Unknown")
            dialog = ResearcherDialog(vm)
            await dialog.vm.call(
                "load", researcher_id=row_data["researcher_id"]
            )  # Copy the selected row's data into the ViewModel
            result = await dialog.show()
            if result == "save":
                await self.vm.call("load")  # Reload the grid after saving

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a researcher has been selected
            await self.vm.call(
                "researcher_selected",
                researcher=row,
                researcher_id=row["researcher_id"],
            )
