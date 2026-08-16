from nicegui import ui


class SQLView:
    def __init__(self):
        with ui.splitter(value=50, horizontal=True).classes("w-full h-full") as splitter:
            with splitter.before:
                ui.codemirror(language="PostgreSQL").classes("w-full h-full")

            with splitter.after:  # as splitter_right:
                grid_def = {
                    "columnDefs": [],
                    # Placeholder for rowData; in a real application, this would be populated from a data source
                    # For example: 'rowData': get_studies_from_database()
                    "rowData": [],
                    "rowSelection": {
                        "mode": "singleRow",
                        "checkboxes": False,
                        "enableClickSelection": True,
                    },
                }
                ui.aggrid(options=grid_def, theme="balham").classes("w-full h-full")