from nicegui import ui
from src.tools.tasks import ManagedTasks
from src.viewmodels import UserListViewModel
from src.viewmodels.sql import SQLViewModel
from src.views.sql_view import SQLView
from src.views.user_view import UserView


class AdminPanel:
    def __init__(self):
        with ui.tabs().props("dense no-caps") as tabs:
            users = ui.tab("Users").classes("text-sky-800")
            sql = ui.tab("SQL").classes("text-sky-800")

        with ui.tab_panels(tabs, value=users, animated=False).classes("w-full h-full"):
            with ui.tab_panel(users).classes("pl-0 pt-0 pb-0 pr-0"):
                vm = UserListViewModel()
                UserView(vm)
                ManagedTasks().create(vm.call("load"))

            with ui.tab_panel(sql).classes("pl-0 pt-0 pb-0 pr-0"):
                vm = SQLViewModel()
                SQLView(vm)
