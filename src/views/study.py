from nicegui import ui
from src.viewmodels.study import StudyListViewModel
from views.study_editor import StudyEditor
from views.study_grid import StudyGrid


class StudyView:
    def __init__(self, view_model: StudyListViewModel):
        self.editor = StudyEditor(view_model.study_vm)
        self.vm = view_model
        self.grid = StudyGrid(self.vm)

    async def load(self):
        await self.vm.load()

    def show(self):
        with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
            with splitter.before:
                self.grid.show()
            with splitter.after:
                self.editor.show()
