from nicegui import ui

from nicemvvm.tools.excel import export_to_excel
from nicemvvm.tools.user import is_user_readonly
from nicemvvm.viewmodels.view_model import ViewModel
from nicemvvm.views.view import View
from src.views.researcher.researcher_study_grid import ResearcherStudyGrid


class ResearcherStudyPanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm=vm)

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("h-full flex-none pl-0"):
                with (
                    ui.button(
                        icon="table_view",
                        on_click=lambda: export_to_excel(
                            self.vm.get("studies"), "researcher_studies.xlsx"
                        ),
                    )
                    .classes("text-xs")
                    .props("padding=xs")
                    .set_enabled(not is_user_readonly())
                ):
                    ui.tooltip("Export to Excel")

            with ui.column().classes("h-full flex-1"):
                ResearcherStudyGrid(self.vm)
