from nicegui import ui

from views.study import study_table_view


def main_view():
    with ui.splitter(value=10).classes("w-full h-screen p-0") as splitter:
        with splitter.before:
            with ui.tabs().props("vertical").classes("w-full") as tabs:
                studies = ui.tab("Studies", icon="science")
                researchers = ui.tab("Researchers", icon="person_outline")
                locations = ui.tab("Locations", icon="apartment")
                reports = ui.tab("Reports", icon="dashboard")
                settings = ui.tab("Settings", icon="settings")

        with splitter.after:
            with (
                ui.tab_panels(tabs, value=studies)
                .props("vertical")
                .classes("size-full")
            ):
                with ui.tab_panel(studies):
                    study_table_view()
                with ui.tab_panel(researchers):
                    ui.label("Researchers").classes("text-h4")
                    ui.label("Content of researchers")
                with ui.tab_panel(locations):
                    ui.label("Locations").classes("text-h4")
                    ui.label("Content of locations")
                with ui.tab_panel(reports):
                    ui.label("Reports").classes("text-h4")
                    ui.label("Content of reports")
                with ui.tab_panel(settings):
                    ui.label("Settings").classes("text-h4")
                    ui.label("Content of settings")
