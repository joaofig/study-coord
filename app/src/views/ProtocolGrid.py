from nicegui import ui
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from src.viewmodels import ProtocolViewModel
from src.viewmodels.ViewModel import ViewModel
from src.views.View import View
from src.views.dialogs.ProtocolDialog import ProtocolDialog


class ProtocolGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid: AgGrid = self._build_grid()

        self.protocols = self.vm.get("protocols")
        if isinstance(self.protocols, ObservableList):
            self.protocols.on_change(self._update_grid)

    def _update_grid(self):
        self.grid.options["rowData"] = self.vm.get("protocols")
        self.grid.update()

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
                        emitEvent('protocol-row-edit', params.data);
                    });
                return btn;
                }
                """
            },
            {"headerName": "Date", "field": "date", "sortable": True, "align": "left", "width": 120},
            {"headerName": "Title", "field": "title", "sortable": True, "align": "left", "flex": 1},
            {"headerName": "Description", "field": "description", "sortable": True, "align": "left", "flex": 2},
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": self.vm.get("protocols"),
            "rowSelection": {"mode": "singleRow", "checkboxes": False, "enableClickSelection": True},
            ":getRowId": "(params) => String(params.data.id)"
        }
        ui.on("protocol-row-edit", self._handle_edit)
        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        return grid

    async def _edit_protocol(self, protocol: dict):
        vm = ProtocolViewModel()
        dlg = ProtocolDialog(vm=vm)
        vm.from_dict(protocol)
        await dlg.show()

    async def _handle_edit(self, event):
        row_data = event.args
        if row_data:
            await self._edit_protocol(row_data)

    def show(self) -> AgGrid:
        return self.grid
