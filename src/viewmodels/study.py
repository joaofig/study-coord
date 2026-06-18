from datetime import date
from nicegui import binding

from models import Study


@binding.bindable_dataclass
class StudyViewModel:
    id: int = 0
    name: str = ""
    sponsor: str = ""
    visits: int = 1
    start_date: str = date.today().strftime("%Y-%m-%d")
    end_date: str = ""
    comments: str = ""

    def copy(self, study: Study):
        self.id = study.id or 0
        self.name = study.name
        self.sponsor = study.sponsor
        self.visits = study.proto_visits
        self.start_date = study.start_date
        self.end_date = study.end_date or ""
        self.comments = study.comments or ""

    def to_study(self) -> Study:
        return Study(
            id=self.id,
            name=self.name,
            sponsor=self.sponsor,
            proto_visits=self.visits,
            start_date=self.start_date,
            end_date=self.end_date,
            comments=self.comments,
        )

    async def save(self):
        study = self.to_study()
        if study.is_valid():
            from db import get_connection
            from db.repository import StudyRepository
            repo = StudyRepository()
            await repo.save(study)
            if study.id:
                self.id = study.id
        else:
            from nicegui import ui
            ui.notify(f"Study is not valid. {study.validation_message()}", color="negative")


