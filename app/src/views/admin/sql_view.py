from nicegui import ui
from nicegui.binding import bind_from
from nicemvvm.tools.excel import export_to_excel
from nicemvvm.viewmodels.view_model import ViewModel
from src.views.admin.sql_grid import SQLGrid
from nicemvvm.views.view import View


class SQLView(View):
    _messages: str = ""

    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none"):
                with (
                    ui.button(on_click=self._run_query, icon="play_circle")
                    .classes("text-xs")
                    .props("padding=xs")
                ):
                    ui.tooltip("Run Query")

                with (
                    ui.button(icon="table_view", on_click=self._on_export_to_excel)
                    .classes("text-xs")
                    .props("padding=xs")
                ):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                with ui.splitter(value=50, horizontal=True).classes(
                    "w-full h-full"
                ) as splitter:
                    with splitter.before:
                        with ui.row().classes("w-full h-full border-1 border-gray-200"):
                            self.editor = (
                                ui.codemirror(language="PostgreSQL")
                                .classes("w-full h-full")
                                .bind_value(vm, "query")
                            )
                            self.editor.map_key("F5", self._run_query)
                            self.editor.map_key("Shift-Enter", self._run_selection)
                            # self.editor.run_method()

                    with splitter.after:
                        with ui.tabs().props("dense no-caps") as self.tabs:
                            result_tab = ui.tab("Result").classes("text-sky-800")
                            messages_tab = ui.tab("Messages").classes("text-sky-800")

                        with ui.tab_panels(
                            self.tabs, value=result_tab, animated=False
                        ).classes("w-full h-full"):
                            with ui.tab_panel(result_tab).classes(
                                "pl-0 pt-0 pb-0 pr-0"
                            ):
                                self.grid = SQLGrid(vm)

                            with ui.tab_panel(messages_tab).classes(
                                "pl-0 pt-0 pb-0 pr-0"
                            ):
                                ui.code(self.vm.get("messages")).classes(
                                    "w-full h-full"
                                ).bind_content(self.vm, "messages")

        bind_from(self, "_messages", vm, "messages", backward=self._on_messages_changed)

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
        export_to_excel(self.vm.get("result"), "query_result.xlsx")

    async def _run_selection(self):
        query = await self.get_selection()
        if query:
            await self.vm.call("run", query=query)
        else:
            ui.notify("No text selected.", color="red")

    def _on_messages_changed(self, messages: str):
        if messages:
            self.tabs.set_value("Messages")  # Switch to the Messages tab
        else:
            self.tabs.set_value("Result")  # Switch to the Result tab

    async def _run_query(self):
        query = await self.get_selection()
        if not query:
            query = self.vm.get("query")
        await self.vm.call("run", query=query)
