from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from tools.messenger import get_messenger
from viewmodels import ResearcherViewModel
from viewmodels.ViewModel import ViewModel
from views.View import View


class ResearcherGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid = self._build_grid()
        self.messenger = get_messenger("researcher")
        self.messenger.subscribe("researcher_saved", self._on_researcher_saved)

    def _build_grid(self) -> AgGrid:
        columns = [
            # {"headerName": "ID", "field": "id", "hide": True},
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
                        emitEvent('resercher-row-edit', params.data);
                    });
                return btn;
                }
                """
            },
            {"headerName": "Number", "field": "number", "sortable": True, "align": "left"},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
            {"headerName": "Phone", "field": "phone", "sortable": True, "align": "left"},
            {"headerName": "Email", "field": "email", "sortable": True, "align": "left"},
            {"headerName": "Comments", "field": "comments", "sortable": True, "align": "left"},
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": [],
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        ui.on("resercher-row-edit", self._handle_edit)
        return ui.aggrid(grid_def).classes("w-full h-full")

    async def _on_researcher_saved(self, **kwargs):
        await self.vm_message("load")  # Reload the grid after a researcher is saved
        self._update_grid()

    def _update_grid(self):
        # Update the grid's rowData with the new list of studies from the ViewModel
        self.grid.options["rowData"] = [s.to_dict() for s in self.vm.get("researchers")]
        self.grid.update()

    async def _handle_notification(self, action: str, **kwargs):
        if action == "list_changed":
            self._update_grid()

    async def _edit_researcher(self, row_data):
        from views.dialogs.ResearcherDialog import ResearcherDialog
        vm = ResearcherViewModel()
        dialog = ResearcherDialog(vm)
        await dialog.vm_message("load", researcher_id=row_data["id"])  # Copy the selected row's data into the ViewModel
        result = await dialog.show()
        if result == "save":
            await self.vm_message("load")  # Reload the grid after saving

    async def _handle_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            await self._edit_researcher(row_data)