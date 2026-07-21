from nicegui import ui
from src.viewmodels.user import UserViewModel
from src.views.View import View

class UserDialog(View):
    def __init__(self, vm: UserViewModel):
        super().__init__(vm)
        
        # Ensure user_role has a default value if not set
        if not self.vm.user_role:
            self.vm.user_role = "User"

        with ui.dialog() as dialog, ui.card().classes("w-120"):
            with ui.row().classes("w-full bg-gray-200 p-2"):
                ui.label("User Details").classes("text-base")
            
            ui.input(label="User Name").classes("w-full").bind_value(self.vm, "user_name")
            
            ui.select(
                label="Role",
                options=["Admin", "User"],
            ).classes("w-full").bind_value(self.vm, "user_role")
            
            ui.input(label="Password", password=True, password_toggle_button=True)\
                .classes("w-full").bind_value(self.vm, "password_1")
                
            ui.input(label="Confirm Password", password=True, password_toggle_button=True)\
                .classes("w-full").bind_value(self.vm, "password_2")

            with ui.row():
                ui.button("Save", on_click=self.save)
                ui.button("Cancel", on_click=lambda: dialog.submit("cancel"))
            self.dialog = dialog

    async def save(self):
        if self.vm.get("password_1") != self.vm.get("password_2"):
            ui.notify("Passwords do not match", kind="error")
            return

        await self.vm.call("save")
        self.dialog.submit("save")

    async def show(self):
        return await self.dialog
