from nicegui import ui, app

from src.tools.tasks import ManagedTasks


async def on_tab_change(event):
    from src.tools.messenger import get_messenger

    match event.value:
        case "Reports":
            messenger = get_messenger("reports")
            await messenger.broadcast("load")


def main_view():
    user_role = app.storage.user.get("user_role", "User")

    with ui.column().classes("w-full h-screen"):
        with ui.tabs().props("dense no-caps") as tabs:
            studies = ui.tab("Studies").classes("text-sky-800")
            researchers = ui.tab("Researchers").classes("text-sky-800")
            reports = ui.tab("Reports").classes("text-sky-800")
            settings = ui.tab("Settings").classes("text-sky-800")
            admin = ui.tab("Admin").classes("text-sky-800")

            # Only visible to Admin users
            admin.set_visibility(user_role == "Admin")

        with ui.tab_panels(tabs, value=studies, animated=False) \
                .classes("h-full w-full"):

            with ui.tab_panel(studies).classes("pl-4 pt-0 pb-0 pr-4"):
                from src.views.StudyView import StudyView
                from src.viewmodels import StudyListViewModel

                vm = StudyListViewModel()
                ManagedTasks().create(vm.load())
                view = StudyView(vm)
                view.show()

            with ui.tab_panel(researchers).classes("pl-4 pt-0 pb-0 pr-4"):
                from src.viewmodels.researcher_list import ResearcherListViewModel
                from src.views.researcher_view import ResearcherView

                vm = ResearcherListViewModel()
                ResearcherView(vm)
                ManagedTasks().create(vm.call("load"))

            with ui.tab_panel(reports).classes("pl-4 pt-0 pb-0 pr-4"):
                from src.views.ReportView import ReportView
                from src.viewmodels.report import ReportViewModel

                vm = ReportViewModel()
                ReportView(vm)
                ManagedTasks().create(vm.call("load"))

            with ui.tab_panel(settings).classes("pl-4 pt-0 pb-0 pr-4"):
                ui.label("Settings").classes("text-h4")
                ui.label("Content of settings")

            with ui.tab_panel(admin).classes("pl-4 pt-0 pb-0 pr-4"):
                if user_role == "Admin":
                    from src.views.UserView import UserView
                    from src.viewmodels import UserListViewModel

                    vm = UserListViewModel()
                    UserView(vm)
                    ManagedTasks().create(vm.call("load"))
