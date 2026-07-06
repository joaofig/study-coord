from nicegui import ui

from src.tools.tasks import ManagedTasks
from src.viewmodels import StudyListViewModel
from src.views.StudyView import StudyView
from viewmodels.ResearcherListViewModel import ResearcherListViewModel
from views.ResearcherView import ResearcherView


def main_view():
    with ui.splitter(value=10).classes("w-full h-screen p-0") as splitter:
        with splitter.before:
            with ui.tabs().props("vertical").classes("w-full").props("dense no-caps") as tabs:
                studies = ui.tab("Studies", icon="science").classes("text-sky-800")
                # visits = ui.tab("Visits", icon="event").classes("text-sky-800")
                # monitoring = ui.tab("Monitoring", icon="monitor_heart").classes("text-sky-800")
                # adverse_events = ui.tab("Adverse Events", icon="dangerous").classes("text-sky-800")
                # patients = ui.tab("Patients", icon="personal_injury").classes("text-sky-800")
                researchers = ui.tab("Researchers", icon="group").classes("text-sky-800")
                reports = ui.tab("Reports", icon="dashboard").classes("text-sky-800")
                settings = ui.tab("Settings", icon="settings").classes("text-sky-800")

        with splitter.after:
            with (
                ui.tab_panels(tabs, value=studies)
                .classes("size-full")
            ):
                with ui.tab_panel(studies):
                    view = StudyView(StudyListViewModel())
                    view.show()
                    ManagedTasks().create(view.load())

                with ui.tab_panel(researchers):
                    vm = ResearcherListViewModel()
                    ResearcherView(vm)
                    ManagedTasks().create(vm.call("load"))

                with ui.tab_panel(reports):
                    ui.label("Reports").classes("text-h4")
                    ui.label("Content of reports")

                with ui.tab_panel(settings):
                    ui.label("Settings").classes("text-h4")
                    ui.label("Content of settings")
