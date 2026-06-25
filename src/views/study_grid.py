from typing import Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from viewmodels.study import StudyListViewModel
from viewmodels.view_model import ViewModel


class StudyGrid:
    def __init__(self, vm: ViewModel) -> None:
        self.vm = vm
        self.grid: Any = None
        vm.register(self._vm_notification)

    async def load(self):
        await self.vm.message("load")
        self._update_grid()

    def _vm_notification(self, action: str, data: Any = None) -> None:
        if action == "list_changed":
            # Update the grid's rowData with the new list of studies from the ViewModel
            self._update_grid()

    def _update_grid(self):
        # Update the grid's rowData with the new list of studies from the ViewModel
        self.grid.options["rowData"] = [s.to_dict() for s in self.vm.get("studies")]
        self.grid.update()

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            # ui.notify(f"{row}")
            await self.vm.message("study_selected", row)
        else:
            # ui.notify('No row selected!')
            await self.vm.message("study_unselected", row)

    def show(self) -> AgGrid:
        columns = [
            {"headerName": "ID", "field": "id", "hide": True},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Sponsor", "field": "sponsor", "sortable": True, "align": "left"},
            {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left"},
            {"headerName": "End", "field": "end_date", "sortable": True, "align": "left"},
            {"headerName": "Patients", "field": "patients", "sortable": True, "align": "right"},
            {"headerName": "Visits", "field": "visits", "sortable": True, "align": "right"},
            {"headerName": "Researchers", "field": "researchers", "sortable": True, "align": "right"},
            {"headerName": "Events", "field": "adverse_events", "sortable": True, "align": "right"},
        ]
        grid_def = {
            "columnDefs": columns,
            # Placeholder for rowData; in a real application, this would be populated from a data source
            # For example: 'rowData': get_studies_from_database()
            "rowData": [],
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        self.grid = ui.aggrid(grid_def).classes("w-full h-full")
        # self.grid.on("rowClicked",
        #              self._row_selected, # ui.notify(event.args["data"]),
        #              ["data"]
        #             )
        self.grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return self.grid

    async def _row_selected(self, event):
        row_data = event.args["data"]
        await self.vm.message("study_selected", row_data)
