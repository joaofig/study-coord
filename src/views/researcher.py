from nicegui import ui


def researcher_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label("Researcher Details").classes("text-h4")
        ui.input(label="Number").classes("w-full")
        ui.input(label="Name").classes("w-full")

        with ui.row():
            ui.button("Save", on_click=lambda: dialog.submit("Save"))
            ui.button("Cancel", on_click=lambda: dialog.submit("Cancel"))
        return dialog


async def show_dialog():
    result = await researcher_dialog()
    ui.notify(f'You chose {result}')


def researcher_grid():
    columns = [
        {"headerName": "Number", "field": "sponsor", "sortable": True, "align": "left"},
        {"headerName": "Name", "field": "name", "sortable": True, "align": "left"},
    ]
    grid_def = {
        "columnDefs": columns,
        "rowData": []
    }
    return ui.aggrid(grid_def)


def researcher_grid_view():
    with ui.row().classes("w-full"):
        with ui.row().classes("w-full"):
            ui.label("Studies").classes("text-h4")
            ui.space()
            ui.button("Add Researcher", on_click=lambda: show_dialog()).props("icon=add")
        researcher_grid()
