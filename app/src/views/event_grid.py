from nicegui import app, ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList
from src.viewmodels import AdverseEventViewModel
from src.viewmodels.view_model import ViewModel
from src.views.dialogs.event_dialog import EventDialog
from src.views.view import View


class EventGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.events = self.vm.get("events")
        if isinstance(self.events, ObservableList):
            self.events.on_change(self._update_grid)

        self.grid: AgGrid = self._build_grid()
        self.subscribe("event", "saved", self._update_grid)

    async def _edit_event(self, event_id: int):
        event_vm = AdverseEventViewModel()
        event_vm.updated_by = app.storage.user.get("username", "Unknown")
        study_id = self.vm.get("study_id")
        patient_id = self.vm.get("patient_id")
        await event_vm.call("load_patients", study_id=study_id)
        await event_vm.call("load", event_id=event_id)
        dialog = EventDialog(event_vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load", study_id=study_id, patient_id=patient_id)
            await self.broadcast("study_list", "load")

    async def _on_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            await self._edit_event(row_data["adverse_event_id"])

    async def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("events")

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "adverse_event_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('event-row-edit', params.data);
                    });
                return btn;
                }
                """,
            },
            {
                "headerName": "Date",
                "field": "date",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Type",
                "field": "event_type",
                "sortable": True,
                "align": "left",
                "width": 120,
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
            {
                "headerName": "Description",
                "field": "description",
                "sortable": True,
                "align": "left",
                "filter": "agTextColumnFilter", "floatingFilter": False,
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.events,
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.selected_id)",
        }
        ui.on("event-row-edit", self._on_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call("event_selected", event_id=row["selected_id"])
        else:
            await self.vm.call("event_unselected")

    def show(self) -> AgGrid:
        return self.grid
