from nicegui import ui, app

from src.viewmodels.view_model import ViewModel
from src.views.View import View
from src.tools.excel import export_to_excel
from src.tools.user import logout
from src.viewmodels import UserViewModel
from src.views.UserGrid import UserGrid
from src.views.dialogs import UserDialog
from src.views.dialogs.delete_warning_dialog import DeleteWarningDialog


class UserView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with ui.button(icon="add", on_click=self._show_dialog) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Add User")

                with ui.button(icon="delete", on_click=self._on_delete_user) \
                        .bind_enabled(self.vm, "selected_id") \
                        .classes("text-xs") \
                        .props("padding=xs color=red"):
                    ui.tooltip("Delete User")

                with ui.button(icon="table_view", on_click=self._on_export_to_excel) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Export to Excel")

                ui.separator()

                with ui.button(icon="logout", on_click=logout) \
                        .classes("text-xs") \
                        .props("padding=xs"):
                    ui.tooltip("Log Out")

            with ui.column().classes("h-full flex-1"):
                self.grid = UserGrid(vm)

    async def _on_delete_user(self):
        user = self.vm.get("selected_row")
        user_name = user.get("user_name", "") if user else ""
        if user_name == app.storage.user.get("username"):
            ui.notify("You cannot delete the currently logged-in user.", color="red")
            return
        if user_name == "admin":
            ui.notify("You cannot delete the admin user.", color="red")
            return

        dialog = DeleteWarningDialog("Are you sure you want to delete this user?")
        result = await dialog.show()
        if result == "delete":
            dialog.close()
            user_id = self.vm.get("selected_id")
            await self.vm.call("delete", user_id=user_id)
            await self.vm.call("load")
            await self.broadcast("user_list", "load")

    async def _show_dialog(self):
        vm = UserViewModel()
        vm.created_by = app.storage.user.get("username", "Unknown")
        vm.updated_by = app.storage.user.get("username", "Unknown")

        dialog = UserDialog(UserViewModel())
        result = await dialog.show()
        if result == "save":
            await self.vm.call("load")

    def _on_export_to_excel(self):
        users = [r.to_dict() for r in self.vm.get("users")]
        if users:
            export_to_excel(users, filename="users.xlsx")
