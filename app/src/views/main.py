from nicegui import app, ui
from src.repositories import UserRepository
from src.tools.tasks import ManagedTasks
from src.tools.user import logout
from src.viewmodels import UserViewModel


async def on_tab_change(event):
    from src.tools.messenger import get_messenger

    match event.value:
        case "Reports":
            messenger = get_messenger("reports")
            await messenger.broadcast("load")


async def study_view():
    from src.viewmodels import StudyListViewModel
    from src.views.study_view import StudyView

    study_vm = StudyListViewModel()
    await study_vm.call("load")
    view = StudyView(study_vm)
    view.show()


async def researcher_view():
    from src.viewmodels import ResearcherListViewModel
    from src.views.researcher_view import ResearcherView

    researcher_vm = ResearcherListViewModel()
    await researcher_vm.call("load")
    ResearcherView(researcher_vm)


async def report_view():
    from src.viewmodels.report import ReportViewModel
    from src.views.report_view import ReportView

    vm = ReportViewModel()
    await vm.call("load")
    ReportView(vm)


async def settings_view(user_id: int):
    from src.views.settings_view import SettingsView

    vm = UserViewModel()
    repo = UserRepository()
    user = await repo.load(user_id)
    if user is not None:
        vm.copy(user)
    SettingsView(vm)
    await vm.call("load")


async def admin_view():
    from src.viewmodels import UserListViewModel
    from src.views.user_view import UserView

    vm = UserListViewModel()
    UserView(vm)
    await vm.call("load")


async def main_view():
    user_role = app.storage.user.get("user_role", "User")
    user_id = app.storage.user.get("user_id", 0)

    with ui.column().classes("w-full h-screen"):
        with ui.row().classes("w-full flex-1"):
            with ui.tabs().props("dense no-caps") as tabs:
                studies = ui.tab("Studies").classes("text-sky-800")
                researchers = ui.tab("Researchers").classes("text-sky-800")
                reports = ui.tab("Reports").classes("text-sky-800")
                settings = ui.tab("Settings").classes("text-sky-800")
                admin = ui.tab("Admin").classes("text-sky-800")

                # Only visible to Admin users
                admin.set_visibility(user_role == "Admin")
            # ui.space()
            with ui.row().classes("w-full flex-1 justify-end"):
                with ui.button(text="Logout", on_click=logout)\
                        .classes("text-xs mr-4 mt-2") \
                        .props("padding=xs"):
                    ui.tooltip("Log Out")


        with ui.tab_panels(tabs, value=studies, animated=False).classes(
            "h-full w-full"
        ):
            with ui.tab_panel(studies).classes("pl-4 pt-0 pb-0 pr-4"):
                await study_view()

            with ui.tab_panel(researchers).classes("pl-4 pt-0 pb-0 pr-4"):
                await researcher_view()

            with ui.tab_panel(reports).classes("pl-4 pt-0 pb-0 pr-4"):
                await report_view()

            with ui.tab_panel(settings).classes("pl-4 pt-0 pb-0 pr-4"):
                await settings_view(user_id)

            with ui.tab_panel(admin).classes("pl-4 pt-0 pb-0 pr-4"):
                if user_role == "Admin":
                    await admin_view()
