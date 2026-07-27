from nicegui import ui

from viewmodels import UserViewModel
from views.dialogs.password_dialog import PasswordDialog
from views.view import View


class SettingsView(View):
    def __init__(self, vm: UserViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("Settings").classes("text-base")

            with ui.row().classes("w-full h-full"):
                ui.button("Change Password", on_click=self._on_change_password)

    async def _on_change_password(self):
        dialog = PasswordDialog(self.vm)
        result = await dialog.show()
        if result == "save":
            await self.vm.call("save")