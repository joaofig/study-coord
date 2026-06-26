from typing import Any

from nicegui import binding

from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class ResearcherViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    comments: str = ""
    role: str = ""

    def __post_init__(self):
        super().__init__()

    async def handle_command(self, msg: str, data: Any = None):
        match msg:
            case "save":
                return None
        return None