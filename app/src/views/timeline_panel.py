from nicegui import ui
from nicegui.observables import ObservableList
from src.viewmodels import ViewModel
from src.views.view import View


class TimelinePanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)

        self.milestones = self.vm.get("milestones")
        if isinstance(self.milestones, ObservableList):
            self.milestones.on_change(self._update_view)

        self.root = ui.row().classes("w-full h-full")

    async def _update_view(self):
        # Clear the existing view root
        self.root.clear()

        with self.root:
            ui.separator()
            with ui.scroll_area().classes("w-full h-full"):
                with ui.timeline(layout="dense", side="right"):
                    # Rebuild the view based on the updated timeline data
                    for milestone in self.milestones:
                        ui.timeline_entry(title=milestone.get("title", ""),
                                          subtitle=milestone.get("subtitle", ""),
                                      icon=milestone.get("icon", ""),
                                      body=milestone.get("description", ""),
                                      color=milestone.get("color", "gray"))

    def show(self):
        return self.root