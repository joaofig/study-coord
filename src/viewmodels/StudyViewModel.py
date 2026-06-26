from nicegui import binding
from nicegui.observables import ObservableSet

from src.db.repository import StudyRepository
from src.models import Study
from src.models.study import StudyRow
from src.viewmodels.ViewModel import ViewModel
from tools.messenger import get_messenger


@binding.bindable_dataclass
class StudyViewModel(ViewModel):
    id: int = 0
    name: str = ""
    sponsor: str = ""
    visits: int = 1
    start_date: str = ""
    end_date: str = ""
    comments: str = ""
    data_changed: bool = False
    change_set = ObservableSet()
    is_old: bool = False

    def __post_init__(self):
        super().__init__()
        self.messenger = get_messenger("study")
        self.messenger.subscribe("study_selected", self._handle_study_selected)

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_study_selected(self, **kwargs):
        study_row = kwargs.get("study")
        if study_row:
            study_id = study_row.get("id")
            if study_id:
                study = await Study.load(study_id=study_id)
                if study:
                    self.copy(study)

    def copy(self, study: Study):
        self.id = study.id or 0
        self.name = study.name
        self.sponsor = study.sponsor
        self.visits = study.proto_visits
        self.start_date = study.start_date
        self.end_date = study.end_date or ""
        self.comments = study.comments or ""
        self.changed = False
        self.is_old = study.id is not None
        self.change_set.clear()

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
            await study.save()
            if study.id:
                self.id = study.id
            self.changed = False
            self.is_old = True
            await self.messenger.send("study_saved", study=study)
            await self.notify("study_saved", study=study)
        else:
            from nicegui import ui
            ui.notify(f"Study is not valid. {study.validation_message()}", color="negative")

    async def handle_command(self, msg: str, **kwargs):
        match msg:
            case "copy":
                await self.copy(kwargs.get("study"))

            case "load":
                study_id = int(kwargs.get("study_id"))
                study = await Study.load(study_id)
                if study:
                    await self.copy(study)

            case "save":
                await self.save()

            case "mark_changed":
                field_name = kwargs.get("field_name")
                if field_name:
                    self._field_changed(field_name)
