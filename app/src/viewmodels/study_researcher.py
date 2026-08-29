from dataclasses import field
from datetime import datetime
from typing import Any

from nicegui import binding
from src.dtos.researcher import (
    ResearcherDTO,
    StudyResearcherDTO,
    study_researcher_roles,
)
from src.models.researcher import ResearcherModel
from src.models.study_researcher import StudyResearcherModel

from .researcher import ResearcherViewModel
from nicemvvm.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class StudyResearcherViewModel(ViewModel):
    sr_id: int = 0
    study_id: int = 0
    researcher_id: int = 0  # Bound to the selector
    role: str = "standard"
    study_comments: str = ""
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""

    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    is_invalid: bool = False
    validation: str = ""

    researcher_list: list[ResearcherDTO] = field(default_factory=list)

    changed: bool = False
    roles: dict = field(default_factory=study_researcher_roles)

    model: StudyResearcherModel = StudyResearcherModel()

    researchers: dict[int, str] = field(default_factory=dict)
    selection: ResearcherViewModel = field(default_factory=ResearcherViewModel)

    def __post_init__(self):
        super().__init__()

    def to_dto(self) -> StudyResearcherDTO:
        return StudyResearcherDTO(
            sr_id=self.sr_id,
            study_id=self.study_id,
            researcher_id=self.researcher_id,
            role=self.role,
            study_comments=self.study_comments,
        )

    def to_dict(self):
        return {
            "sr_id": self.sr_id,
            "study_id": self.study_id,
            "researcher_id": self.researcher_id,
            "role": self.role,
            "study_comments": self.study_comments,
            "number": self.number,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }

    def from_dict(self, data: dict):
        self.sr_id = data.get("sr_id") or data.get("id") or 0
        self.study_id = data.get("study_id", 0)
        self.researcher_id = data.get("researcher_id", 0)
        self.role = data.get("role", "standard")
        self.study_comments = data.get("study_comments", "")
        self.number = data.get("number", "")
        self.name = data.get("name", "")
        self.phone = data.get("phone", "")
        self.email = data.get("email", "")

        self.selection.researcher_id = self.researcher_id
        self.selection.name = self.name
        self.selection.number = self.number
        self.selection.phone = self.phone
        self.selection.email = self.email

    async def save(self):
        sr = self.to_dto()
        sr.log_change(self.sr_id)
        await self.model.save(sr)
        if sr.sr_id:
            self.sr_id = sr.sr_id
        self.changed = False
        await self.broadcast("study_researcher", "saved")

    async def _on_call(self, msg: str, **kwargs) -> Any:
        """
        Handle incoming messages from the attached View.

        :param msg: The message to handle.
        :param kwargs: Additional keyword arguments.
        :return: None
        """
        match msg:
            case "save":
                return await self.save()

            case "validate":
                return await self.validate()

            case "load":
                rs = [
                    r
                    for r in self.researcher_list
                    if r.researcher_id == self.researcher_id
                ]
                if len(rs) > 0:
                    researcher = rs[0]
                    self.selection.copy(researcher)
                    self.number = researcher.number
                    self.name = researcher.name
                    self.phone = researcher.phone
                    self.email = researcher.email
                else:
                    self.number = ""

        return None

    async def load_researchers(self):
        model = ResearcherModel()
        self.researcher_list = await model.list()
        self.researchers = {sr.researcher_id: sr.name for sr in self.researcher_list}

    async def validate(self) -> bool:
        self.validation = ""
        self.is_invalid = False

        if not self.researcher_id or self.researcher_id == 0:
            self.validation += "**Researcher** is required  \r\n"

        if not self.role:
            self.validation += "**Role** is required  \r\n"
        elif self.role not in self.roles:
            self.validation += "**Role** is invalid  \r\n"

        self.is_invalid = len(self.validation) > 0
        return not self.is_invalid
