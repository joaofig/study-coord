from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from src.viewmodels import StudyViewModel
from src.viewmodels.view_model import ViewModel
from src.views.View import View
from src.views.dialogs.study import StudyDialog


class StudyGrid(View):
    def __init__(self, vm: ViewModel) -> None:
        super().__init__(vm)
        self.grid = self._build_grid()
        self.studies = self.vm.get("studies")
        if isinstance(self.studies, ObservableList):
            self.studies.on_change(self._update_grid)

    async def load(self):
        await self.vm.call("load")

    def _update_grid(self):
        # Update the grid's rowData with the new list of studies from the ViewModel
        self.grid.options["rowData"] = self.vm.get("studies")
        self.grid.update()

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a study has been selected
            await self.vm.call("study_selected", study=row, study_id=row["id"])
        else:
            await self.vm.call("study_unselected")

    async def _on_edit(self, event):
        # Handle the edit button click event from the AgGrid component
        row = event.args
        if row:
            vm = StudyViewModel()
            dialog = StudyDialog(vm)
            await vm.call("load", study_id=row["id"])
            result = await dialog.show()
            if result == "save":
                await self.vm.call("load")  # Reload the grid after saving

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
                    emitEvent('study-row-edit', params.data);
                });
                return btn;
            }
            """
            },
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Sponsor", "field": "sponsor", "sortable": True, "align": "left"},
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left", "width": 90},
            {"headerName": "End", "field": "end_date", "sortable": True, "align": "left", "width": 90},
            {"headerName": "Patients", "field": "patients", "sortable": True, "align": "right"},
            {"headerName": "Visits", "field": "protocol_visits", "sortable": True, "align": "right"},
            {"headerName": "Researchers", "field": "researchers", "sortable": True, "align": "right"},
            {"headerName": "Events", "field": "events", "sortable": True, "align": "right"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        ui.on("study-row-edit", self._on_edit)
        self.grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        # self.grid.on("rowClicked",
        #              self._row_selected, # ui.notify(event.args["data"]),
        #              ["data"]
        #             )
        self.grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return self.grid

    def show(self) -> AgGrid:
        return self.grid