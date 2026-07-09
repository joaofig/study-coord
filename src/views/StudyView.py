from nicegui import ui

from viewmodels.ViewModel import ViewModel
from views.StudyGrid import StudyGrid
from views.StudyPanel import StudyPanel
from views.View import View


class StudyView(View):
    """
    This is the main Study view, which contains the StudyGrid and StudyEditor components.
    It is responsible for managing the layout and interactions between these components.
    """
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        self.grid = StudyGrid(vm)

    async def load(self):
        await self.vm.call("load")

    async def _on_delete_study(self):
        pass

    async def _new_study_dialog(self):
        pass

    def show(self):
        with ui.splitter(horizontal=True).classes("w-full h-full") as splitter:
            with splitter.before:
                with ui.row().classes("w-full h-full"):
                    with ui.column().classes("h-full flex-none pl-0"):
                        with ui.button(icon="add", on_click=lambda: self._new_study_dialog()) \
                                .classes("text-xs") \
                                .props("padding=xs"):
                            ui.tooltip("Add Study")
                        with ui.button(icon="delete", on_click=lambda: self._on_delete_study()) \
                                .bind_enabled(self.vm, "selected_id") \
                                .classes("text-xs") \
                                .props("color=red padding=xs"):
                            ui.tooltip("Delete Study")
                        with ui.button(icon="table_view").classes("text-xs") \
                                .props("padding=xs"):
                            ui.tooltip("Export to Excel")

                    with ui.column().classes("h-full flex-1"):
                        self.grid.show()

            with splitter.after:
                StudyPanel(self.vm)
