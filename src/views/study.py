from nicegui import ui
from nicegui.elements.aggrid import AgGrid


def study_editor():
    # ui.label("Study Details").classes("text-h5")

    with ui.tabs() as tabs:
        study = ui.tab(name="Study", icon="science").classes("text-sky-600")
        visits = ui.tab(name="Visits", icon="event").classes("text-sky-600")
        monitoring = ui.tab(name="Monitoring", icon="monitor_heart").classes("text-sky-600")
        adverse_events = ui.tab(name="Events", icon="dangerous").classes("text-sky-600")
        patients = ui.tab(name="Patients", icon="personal_injury").classes("text-sky-600")
        researchers = ui.tab(name="Researchers", icon="group").classes("text-sky-600")
    with (
        ui.tab_panels(tabs, value=study)
                .props("vertical")
                .classes("size-full")
    ):
        with ui.tab_panel(study):
            ui.input(label="Name").classes("w-full")
            ui.input(label="Sponsor").classes("w-full")

            with ui.row().classes("gap-2"):
                ui.date_input(label="Start Date")
                ui.date_input(label="End Date")

            with ui.row().classes("gap-2"):
                (ui.number(label="Protocol Visits", value=1)
                 .props('clearable')
                 .classes("w-full")
                 )
            with ui.row().classes("gap-2 w-full"):
                ui.textarea(label="Description").classes("w-full")


def study_dialog():
    with ui.dialog().props("full-width full-height") as dialog, ui.card():
        study_editor()

        with ui.row():
            ui.button("Save", on_click=lambda: dialog.submit("Save"))
            ui.button("Cancel", on_click=lambda: dialog.submit("Cancel"))
        return dialog


async def show_dialog():
    result = await study_dialog()
    ui.notify(f'You chose {result}')


def study_grid() -> AgGrid:
    columns = [
        {"headerName": "ID", "field": "id", "hide": True},
        {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
        {"headerName": "Sponsor", "field": "sponsor", "sortable": True, "align": "left"},
        {"headerName": "Start", "field": "start_date", "sortable": True, "align": "left"},
        {"headerName": "End", "field": "end_date", "sortable": True, "align": "left"},
        {"headerName": "Patients", "field": "patients", "sortable": True, "align": "right"},
        {"headerName": "Visits", "field": "visits", "sortable": True, "align": "right"},
        {"headerName": "Researchers", "field": "researchers", "sortable": True, "align": "right"},
        {"headerName": "Events", "field": "adverse_events", "sortable": True, "align": "right"},
    ]
    grid_def = {
        "columnDefs": columns,
        "rowData": []
    }
    return ui.aggrid(grid_def)


def study_grid_view():
    with ui.row().classes("w-full"):
        ui.label("Studies").classes("text-h4")
        ui.space()
        ui.button("Add Study", on_click=lambda: show_dialog()).props("icon=add")
    with ui.row().classes("w-full h-full"):
        study_grid().classes("w-full h-full")


def study_view():
    with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
        with splitter.before:
            study_grid_view()
        with splitter.after:
            study_editor()


