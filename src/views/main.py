from nicegui import ui

from src.tools.tasks import ManagedTasks
from src.viewmodels.study import StudyListViewModel
from src.views.researcher import researcher_grid_view
from src.views.study import StudyView


def main_view():
    with ui.splitter(value=10).classes("w-full h-screen p-0") as splitter:
        with splitter.before:
            with ui.tabs().props("vertical").classes("w-full") as tabs:
                studies = ui.tab("Studies", icon="science").classes("text-sky-800")
                visits = ui.tab("Visits", icon="event").classes("text-sky-800")
                monitoring = ui.tab("Monitoring", icon="monitor_heart").classes("text-sky-800")
                adverse_events = ui.tab("Adverse Events", icon="dangerous").classes("text-sky-800")
                patients = ui.tab("Patients", icon="personal_injury").classes("text-sky-800")
                researchers = ui.tab("Researchers", icon="group").classes("text-sky-800")
                reports = ui.tab("Reports", icon="dashboard").classes("text-sky-800")
                settings = ui.tab("Settings", icon="settings").classes("text-sky-800")

        with splitter.after:
            with (
                ui.tab_panels(tabs, value=studies)
                .props("vertical")
                .classes("size-full")
            ):
                with ui.tab_panel(studies):
                    view = StudyView(StudyListViewModel())
                    view.show()
                    ManagedTasks().create(view.load())

                with ui.tab_panel(visits):
                    ui.label("Visits").classes("text-h4")
                    ui.label("Content of visits")

                with ui.tab_panel(monitoring):
                    ui.label("Monitoring").classes("text-h4")
                    ui.label("Content of monitoring")

                with ui.tab_panel(adverse_events):
                    ui.label("Adverse Events").classes("text-h4")
                    ui.label("Content of adverse events")

                with ui.tab_panel(patients):
                    ui.label("Patients").classes("text-h4")
                    ui.label("Content of patients")

                with ui.tab_panel(researchers):
                    researcher_grid_view()

                with ui.tab_panel(reports):
                    ui.label("Reports").classes("text-h4")
                    ui.label("Content of reports")
                with ui.tab_panel(settings):
                    ui.label("Settings").classes("text-h4")
                    ui.label("Content of settings")
