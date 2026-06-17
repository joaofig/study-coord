from nicegui import ui
from nicegui.elements.table import Table


def study_table() -> Table:
    columns = [
        {"name": "id", "field": "id", "required": False},
        {
            "name": "name",
            "label": "Study Name",
            "field": "name",
            "sortable": True,
            "align": "left",
        },
        {
            "name": "location",
            "label": "Site",
            "field": "location",
            "sortable": True,
            "align": "left",
        },
        {
            "name": "start_date",
            "label": "Start Date",
            "field": "start_date",
            "sortable": True,
            "align": "left",
        },
        {"name": "id_del", "field": "id", "required": False},
    ]

    rows = [
        {
            "id": 1,
            "name": "Study 1",
            "location": "Location 1",
            "start_date": "2023-01-01",
            "id_del": 1,
        },
    ]
    table = ui.table(columns=columns, rows=rows).props("dense")
    table.row_key = "id"
    with table.add_slot("body-cell-id"):
        with table.cell("id"):
            ui.button(icon="edit").props("flat").on(
                "click",
                js_handler="() => emit(props.row.name)",
                handler=lambda e: ui.notify(e.args),
            )
        with table.add_slot("body-cell-id_del"):
            with table.cell("id"):
                ui.button(icon="delete_forever").props("flat").on(
                    "click",
                    js_handler="() => emit(props.row.name)",
                    handler=lambda e: ui.notify(e.args),
                )
    return table


def study_table_view():
    with ui.row().classes("w-full"):
        with ui.row().classes("w-full"):
            ui.label("Studies").classes("text-h4")
            ui.space()
            ui.button("Add Study")
        table = study_table()
        # table.set_selection("single")


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
            ui.button("Add Study")
        grid = study_grid()
