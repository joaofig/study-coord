from nicegui import ui

from src.tools.tasks import ManagedTasks
from src.viewmodels import StudyListViewModel
from src.views.StudyView import StudyView
from viewmodels.ResearcherListViewModel import ResearcherListViewModel
from views.ResearcherView import ResearcherView


def main_view():
    with ui.tabs().props("dense no-caps") as tabs:
        studies = ui.tab("Studies").classes("text-sky-800")
        researchers = ui.tab("Researchers").classes("text-sky-800")
        reports = ui.tab("Reports").classes("text-sky-800")
        settings = ui.tab("Settings").classes("text-sky-800")

    with ui.tab_panels(tabs, value=studies).classes("h-screen w-full"):

        with ui.tab_panel(studies):
            vm = StudyListViewModel()
            ManagedTasks().create(vm.load())
            view = StudyView(vm)
            view.show()

        with ui.tab_panel(researchers):
            # ui.label("Researchers").classes("text-h4")
            # ui.label("Content of researchers")
            vm = ResearcherListViewModel()
            ResearcherView(vm)
            ManagedTasks().create(vm.call("load"))

        with ui.tab_panel(reports):
            ui.label("Reports").classes("text-h4")
            ui.label("Content of reports")

        with ui.tab_panel(settings):
            ui.label("Settings").classes("text-h4")
            ui.label("Content of settings")
