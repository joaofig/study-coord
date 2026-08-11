from datetime import datetime
from typing import Any

from nicegui import binding
from nicegui.observables import ObservableSet
from src.dtos.researcher import ResearcherDTO
from src.models.researcher import ResearcherModel
from src.tools.validation import is_email
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class ResearcherViewModel(ViewModel):
    researcher_id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    is_invalid: bool = False
    validation: str = ""

    data_changed: bool = False
    change_set = ObservableSet()
    is_old: bool = False
    model: ResearcherModel = ResearcherModel()

    def __post_init__(self):
        super().__init__()
        self.subscribe(
            "researcher", "researcher_selected", self._handle_researcher_selected
        )

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_researcher_selected(self, **kwargs):
        researcher_row = kwargs.get("researcher")
        if researcher_row:
            researcher_id = researcher_row.get("researcher_id")
            if researcher_id:
                researcher = await self.model.load(researcher_id=int(researcher_id))
                if researcher:
                    self.copy(researcher)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "copy":
                self.copy(kwargs.get("researcher"))

            case "save":
                await self.save()

            case "load":
                if "researcher_id" in kwargs:
                    r = await self.model.load(
                        researcher_id=kwargs.get("researcher_id", 0)
                    )
                    if r:
                        self.copy(r)

            case "validate":
                return await self.validate()
        return None

    def copy(self, researcher: ResearcherDTO):
        self.researcher_id = researcher.researcher_id
        self.name = researcher.name
        self.number = researcher.number
        self.phone = researcher.phone
        self.email = researcher.email
        self.comments = researcher.comments or ""
        self.data_changed = False
        self.is_old = researcher.researcher_id > 0
        self.change_set.clear()
        self.created_at = researcher.created_at
        self.created_by = researcher.created_by
        self.updated_at = researcher.updated_at
        self.updated_by = researcher.updated_by

    def to_dto(self) -> ResearcherDTO:
        return ResearcherDTO(
            researcher_id=self.researcher_id,
            number=self.number,
            name=self.name,
            phone=self.phone,
            email=self.email,
            comments=self.comments,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    async def save(self):
        researcher = self.to_dto()
        researcher.log_change(self.researcher_id)
        await self.model.save(researcher)
        if researcher.researcher_id:
            self.researcher_id = researcher.researcher_id
        self.data_changed = False
        self.is_old = True

    async def validate(self) -> str | None:
        self.is_invalid = False
        self.validation = ""

        if self.researcher_id == 0:
            if await self.model.number_exists(self.number):
                self.validation += "**Researcher Number** already exists.  \r\n"

        if not self.number or len(self.number.strip()) == 0:
            self.validation += "**Researcher Number** is required.  \r\n"

        if not self.name or len(self.name.strip()) == 0:
            self.validation += "**Researcher Name** is required.  \r\n"
        if len(self.name) < 3:
            self.validation += "**Researcher Name** must be at least 3 characters long.  \r\n"
        if len(self.name) > 128:
            self.validation += "**Researcher Name** must be at most 128 characters long.  \r\n"

        if self.email and not is_email(self.email):
            self.validation += "**Researcher Email** is invalid.  \r\n"

        self.is_invalid = len(self.validation) > 0
