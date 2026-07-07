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

    def show(self):
        with ui.splitter(horizontal=True).classes("w-full h-full") as splitter:
            with splitter.before:
                self.grid.show()

            with splitter.after:
                StudyPanel(self.vm)
