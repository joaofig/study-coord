from datetime import date
from nicegui import binding


@binding.bindable_dataclass
class StudyViewModel:
    id: int = 0
    name: str = ""
    sponsor: str = ""
    start_date: str = date.today().strftime("%Y-%m-%d")
    end_date: str = ""
