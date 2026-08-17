from nicegui import ui

from src.viewmodels import ViewModel
from src.views.sql_grid import SQLGrid
from src.views.view import View


class SQLView(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with ui.button(on_click=self._run_query, icon="play_circle") \
                    .classes("text-xs") \
                    .props("padding=xs"):
                    ui.tooltip("Run Query")

                with ui.button(icon="table_view", on_click=self._on_export_to_excel) \
                    .classes("text-xs") \
                    .props("padding=xs"):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                with ui.splitter(value=50, horizontal=True).classes("w-full h-full") as splitter:
                    with splitter.before:
                        with ui.row().classes("w-full h-full border-1 border-gray-200"):
                            self.editor = ui.codemirror(language="PostgreSQL") \
                                .classes("w-full h-full") \
                                .bind_value(vm, "query")
                            # self.editor.run_method()

                    with splitter.after:
                        SQLGrid(vm)

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

    async def _on_export_to_excel(self):
        print("Export to Excel")

    async def _run_query(self):
        query = await self.get_selection()
        if not query:
            query = self.vm.get("query")
        await self.vm.call("run", query=query)
