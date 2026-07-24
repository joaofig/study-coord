from dataclasses import field
from typing import Dict, Any

from nicegui import binding

from src.dtos.researcher import StudyResearcherDTO
from src.models import StudyResearcherModel
from src.models.researcher import study_researcher_roles
from .researcher import ResearcherViewModel
from .view_model import ViewModel


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
    changed: bool = False
    roles: dict = field(default_factory=study_researcher_roles)

    model: StudyResearcherModel = StudyResearcherModel()

    researchers: Dict[int, str] = field(default_factory=dict)
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

            case "load":
                sr = await self.model.load(self.researcher_id)
                if sr and sr.researcher:
                    self.selection.copy(sr.researcher)
                    self.number = sr.researcher.number
                    self.name = sr.researcher.name
                    self.phone = sr.researcher.phone
                    self.email = sr.researcher.email

        return None

    async def load_researchers(self):
        researcher_list = await self.model.list(self.study_id)
        self.researchers = {
            sr.researcher_id: sr.researcher.name
            for sr in researcher_list
            if sr.researcher
        }
