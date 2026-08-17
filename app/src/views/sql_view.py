from nicegui import ui

from src.viewmodels import ViewModel
from src.views.view import View


class SQLView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        with ui.splitter(value=50, horizontal=True).classes("w-full h-full") as splitter:
            with splitter.before:
                with ui.row().classes("w-full"):
                    ui.button(on_click=self.run_query).props("icon=play") \
                        .classes("text-xs") \
                        .props("padding=xs")
                with ui.row().classes("w-full"):
                    self.editor = ui.codemirror(language="PostgreSQL") \
                        .classes("w-full h-full") \
                        .bind_value(vm, "query")
                    # self.editor.run_method()

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

    async def get_selection(self) -> str:
        selected_text = await ui.run_javascript(f'''
            (function() {{
                const cm = getElement("{self.editor.id}");
                const state = cm.editor.state;
                const sel = state.selection.main;
                return state.doc.slice(sel.from, sel.to).toString();
            }})()
        ''')
        return selected_text

    async def run_query(self):
        query = await self.get_selection()
        if query:
            print(query)
        else:
            print(self.vm.get("query"))
