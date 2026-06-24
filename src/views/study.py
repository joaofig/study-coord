from nicegui import ui

from viewmodels.view_model import ViewModel
from views.study_editor import StudyEditor
from views.study_grid import StudyGrid


class StudyView:
    """
    This is the main Study view, which contains the StudyGrid and StudyEditor components.
    It is responsible for managing the layout and interactions between these components.
    """
    def __init__(self, grid_vm: ViewModel, edit_vm: ViewModel):
        self.grid_vm = grid_vm
        self.edit_vm = edit_vm
        self.grid = StudyGrid(grid_vm)

    async def load(self):
        await self.grid_vm.message("load")

    def show(self):
        with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
            with splitter.before:
                self.grid.show()
            with splitter.after:
                editor = StudyEditor(self.edit_vm)
                editor.show()
