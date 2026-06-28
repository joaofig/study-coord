from typing import Any

from nicegui import binding
from nicegui.observables import ObservableSet

from models import Researcher
from tools.messenger import get_messenger
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class ResearcherViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""
    role: str = ""
    data_changed: bool = False
    change_set = ObservableSet()
    is_old: bool = False

    def __post_init__(self):
        super().__init__()
        self.messenger = get_messenger("researcher")
        self.messenger.subscribe("researcher_selected", self._handle_researcher_selected)

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_researcher_selected(self, **kwargs):
        study_row = kwargs.get("study")
        if study_row:
            study_id = study_row.get("id")
            if study_id:
                study = await Researcher.load(researcher_id=study_id)
                if study:
                    self.copy(study)

    async def handle_command(self, msg: str, data: Any = None):
        match msg:
            case "save":
                return None
        return None