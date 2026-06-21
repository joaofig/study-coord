from datetime import date
from typing import Any

from nicegui import binding

from viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class StudyViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    study_name: str = ""
    study_sponsor: str = ""
    number: str = ""
    start_date: str = date.today().strftime("%Y-%m-%d")
    exit_date: str = ""
    status: str = "active"
    comments: str = ""

    def __post_init__(self):
        super().__init__()

    async def async_message(self, msg: str, data: Any = None):
        pass

    def message(self, msg: str, data: Any = None):
        """No implementation for synchronous messages in StudyViewModel"""
        pass
