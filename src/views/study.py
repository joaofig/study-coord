from nicegui import ui


def study_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label("Study Details").classes("text-h5")
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

        with ui.row():
            ui.button("Save", on_click=lambda: dialog.submit("Save"))
            ui.button("Cancel", on_click=lambda: dialog.submit("Cancel"))
        return dialog


async def show_dialog():
    result = await study_dialog()
    ui.notify(f'You chose {result}')


def study_grid():
    columns = [
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
        with ui.row().classes("w-full"):
            ui.label("Studies").classes("text-h4")
            ui.space()
            ui.button("Add Study", on_click=lambda: show_dialog()).props("icon=add")
        study_grid()
