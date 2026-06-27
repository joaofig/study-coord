from typing import Any

from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from tools.messenger import get_messenger
from viewmodels.ViewModel import ViewModel
from views.View import View


class StudyGrid(View):
    def __init__(self, vm: ViewModel) -> None:
        super().__init__(vm)
        self.grid: Any = None
        self.messenger = get_messenger("study")

    async def load(self):
        await self.command("load")

    def _handle_notification(self, action: str, **kwargs):
        """Handle notifications from the ViewModel"""
        if action == "list_changed":
            self._update_grid()

    def _update_grid(self):
        # Update the grid's rowData with the new list of studies from the ViewModel
        self.grid.options["rowData"] = [s.to_dict() for s in self.vm.get("studies")]
        self.grid.update()

    async def _row_selection_changed(self, event):
        # Handle the row selection change event from the AgGrid component
        row = await self.grid.get_selected_row()
        if row:
            # Notify other components that a study has been selected
            await self.messenger.send("study_selected", study=row, study_id=row["id"])
        else:
            await self.command("study_unselected")

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
