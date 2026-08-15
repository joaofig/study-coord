from datetime import date
from typing import Any

from nicegui import binding, ui
from nicegui.observables import ObservableSet
from src.dtos.study import StudyDTO
from src.models.study import StudyModel
from src.tools.validation import is_date
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class StudyViewModel(ViewModel):
    study_id: int = 0
    protocol: str = ""
    name: str = ""
    sponsor: str = ""
    protocol_visits: int = 1
    start_date: str = date.today().isoformat()
    end_date: str | None = None
    comments: str = ""

    is_invalid: bool = False
    validation: str = ""

    change_set = ObservableSet()
    changed = False
    is_old: bool = False
    model: StudyModel = StudyModel()

    def __post_init__(self):
        super().__init__()

    def copy(self, study: StudyDTO):
        self.study_id = study.study_id or 0
        self.protocol = study.protocol
        self.name = study.name
        self.sponsor = study.sponsor
        self.protocol_visits = study.protocol_visits
        self.start_date = study.start_date.isoformat()
        self.end_date = study.end_date.isoformat() if study.end_date else None
        self.comments = study.comments or ""

        self.changed = False
        self.is_old = study.study_id is not None
        self.change_set.clear()

    def to_dto(self) -> StudyDTO:
        return StudyDTO(
            study_id=self.study_id or 0,
            protocol=self.protocol,
            name=self.name,
            sponsor=self.sponsor,
            protocol_visits=int(self.protocol_visits),
            start_date=date.fromisoformat(self.start_date),
            end_date=None if not self.end_date else date.fromisoformat(self.end_date),
            comments=self.comments,
        )

    async def save(self):
        if not await self._validate():
            ui.notify(self.validation, color="negative")
            return
        study = self.to_dto()
        study.log_change(self.study_id)
        study = await self.model.save(study)
        self.study_id = study.study_id
        await self.broadcast("study", "saved", study_id=self.study_id)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                study_id = kwargs.get("study_id", 0)
                study = await self.model.load(int(study_id))
                if study:
                    self.copy(study)

            case "save":
                await self.save()

            case "validate":
                return await self._validate()

        return None

    async def _validate(self) -> bool:
        self.is_invalid = False
        self.validation = ""

        if not self.protocol or len(self.protocol.strip()) == 0:
            self.validation += "Protocol is required.  \r\n"
        elif len(self.protocol) < 3:
            self.validation += "Protocol must be at least 3 characters long.  \r\n"
        elif len(self.protocol) > 64:
            self.validation += "Protocol must be at most 64 characters long.  \r\n"

        if not self.name or len(self.name.strip()) == 0:
            self.validation += "Study name is required.  \r\n"

        if self.study_id == 0 and await self.model.study_exists(self.name):
            self.validation += "Study name already exists.  \r\n"

        if not self.sponsor or len(self.sponsor.strip()) == 0:
            self.validation += "Sponsor is required.  \r\n"
        elif len(self.sponsor) < 3:
            self.validation += "Sponsor must be at least 3 characters long.  \r\n"
        elif len(self.sponsor) > 128:
            self.validation += "Sponsor must be at most 128 characters long.  \r\n"

        if self.protocol_visits < 1:
            self.validation += "Protocol visits must be at least 1.  \r\n"

        if not self.start_date or not is_date(self.start_date):
            self.validation += "Start date must be a valid date.  \r\n"

        if self.end_date and not is_date(self.end_date):
            self.validation += "End date must be a valid date.  \r\n"

        if not self.start_date:
            self.validation += "Start date is required.  \r\n"

        if self.end_date and self.start_date and self.end_date < self.start_date:
            self.validation += "End date must be after Start date.  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid
