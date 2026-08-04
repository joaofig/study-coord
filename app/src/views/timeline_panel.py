from src.viewmodels import ViewModel
from src.views.view import View


class TimelinePanel(View):
    def __init__(self, vm: ViewModel):
        super().__init__(vm)
        