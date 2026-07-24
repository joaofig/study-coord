from nicegui import ui, app
from nicegui.elements.aggrid import AgGrid
from nicegui.observables import ObservableList

from src.viewmodels import UserViewModel
from src.viewmodels.view_model import ViewModel
from src.views.View import View


class UserGrid(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid = self._build_grid()

        self.users = self.vm.get("users")
        if isinstance(self.users, ObservableList):
            self.users.on_change(self._update_grid)

    def _build_grid(self) -> AgGrid:
        columns = [
            {
                "headerName": "Edit",
                "field": "user_id",
                "width": 50,
                ":cellRenderer": """
                (params) => {
                    const btn = document.createElement('button');
                    btn.innerText = '✏️';
                    btn.style.cssText = 'cursor:pointer; padding:2px 8px;';
                    btn.addEventListener('click', () => {
                        emitEvent('user-row-edit', params.data);
                    });
                return btn;
                }
                """,
            },
            {
                "headerName": "User Name",
                "field": "user_name",
                "sortable": True,
                "align": "left",
            },
            {
                "headerName": "Role",
                "field": "user_role",
                "sortable": True,
                "align": "left",
            },
            {
                "headerName": "Created At",
                "field": "created_at",
                "sortable": True,
                "align": "left",
            },
            {
                "headerName": "Created By",
                "field": "created_by",
                "sortable": True,
                "align": "left",
            },
            {
                "headerName": "Updated At",
                "field": "updated_at",
                "sortable": True,
                "align": "left",
            },
            {
                "headerName": "Updated By",
                "field": "updated_by",
                "sortable": True,
                "align": "left",
            },
        ]
        grid_def = {
            "columnDefs": columns,
            "rowData": [],
            "rowSelection": {
                "mode": "singleRow",
                "checkboxes": False,
                "enableClickSelection": True,
            },
            ":getRowId": "(params) => String(params.data.user_id)",
        }
        ui.on("user-row-edit", self._on_edit)

        grid = ui.aggrid(grid_def, theme="balham").classes("w-full h-full")
        grid.on("selectionChanged", lambda event: self._row_selection_changed(event))
        return grid

    def _update_grid(self):
        self.grid.options["rowData"] = [u.to_dict() for u in self.users]
        self.grid.update()

    async def _on_edit(self, event):
        row_data = event.args  # dict with the full row's data
        if row_data:
            from src.views.dialogs.user_dialog import UserDialog

            vm = UserViewModel()
            vm.updated_by = app.storage.user.get("username", "Unknown")
            dialog = UserDialog(vm)
            await dialog.vm.call("load", user_id=row_data["user_id"])
            result = await dialog.show()
            if result == "save":
                await self.vm.call("load")

    async def _row_selection_changed(self, event):
        row = await self.grid.get_selected_row()
        if row:
            await self.vm.call("user_selected", user=row, user_id=row["user_id"])
