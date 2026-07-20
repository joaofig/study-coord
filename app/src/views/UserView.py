from nicegui import ui

from src.viewmodels.view_model import ViewModel
from src.views.View import View
from tools.excel import export_to_excel
from viewmodels import UserViewModel
from views.UserGrid import UserGrid
from views.dialogs import UserDialog
from views.dialogs.DeleteWarningDialog import DeleteWarningDialog


class UserView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=self._show_dialog) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add User")

                with ui.button(icon="delete") \
                        .bind_enabled(self.vm, "selected_id") \
                        .classes("text-xs") \
                        .props("padding=xs color=red"):
                    ui.tooltip("Delete User")

                with ui.button(icon="table_view", on_click=self._on_export_to_excel) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                self.grid = UserGrid(vm)

    async def _on_delete_user(self):
        dialog = DeleteWarningDialog("Are you sure you want to delete this researcher?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            user_id = self.vm.get("user_id")
            await self.vm.call("delete_user", researcher_id=user_id)
            await self.vm.call("load")
            await self.broadcast("user_list", "load")

    async def _show_dialog(self):
        dialog = UserDialog(UserViewModel())
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    def _on_export_to_excel(self):
        users = [r.to_dict() for r in self.vm.get("users")]
        if users:
            export_to_excel(users, filename="users.xlsx")
