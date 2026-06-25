from nicegui import ui

from viewmodels.study import StudyListViewModel, StudyViewModel
from viewmodels.view_model import ViewModel
from views.study_editor import StudyEditor
from views.study_grid import StudyGrid


class StudyView:
    """
    This is the main Study view, which contains the StudyGrid and StudyEditor components.
    It is responsible for managing the layout and interactions between these components.
    """
    def __init__(self):
        self.grid = StudyGrid(StudyListViewModel())

    async def load(self):
        await self.grid.load()

    def show(self):
        with ui.splitter(horizontal=True, value=50).classes("w-full h-full") as splitter:
            with splitter.before:
                self.grid.show()
            with splitter.after:
                editor = StudyEditor(StudyViewModel())
                editor.show()
