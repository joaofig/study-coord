from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from viewmodels.ViewModel import ViewModel
from views.View import View


class ResearcherGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid = self._build_grid()

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
            {"headerName": "Number", "field": "sponsor", "sortable": True, "align": "left"},
            {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
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

    async def _handle_edit(self, event):
        ...
        # row_data = event.args  # dict with the full row's data
        # if row_data:
        #     await self._edit_patient(row_data)
        # ui.notify(f"Edit triggered for: {row_data["number"]} (id={row_data['id']})")