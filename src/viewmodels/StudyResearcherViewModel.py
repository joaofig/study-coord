from dataclasses import field
from typing import Dict, Any

from nicegui import binding

from models.researcher import StudyResearcher, Researcher, ResearcherList, study_researcher_roles
from .ResearcherViewModel import ResearcherViewModel
from .ViewModel import ViewModel


@binding.bindable_dataclass
class StudyResearcherViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    researcher_id: int = 0      # Bound to the selector
    role: str = "standard"
    study_comments: str = ""
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    changed: bool = False
    roles: dict = field(default_factory=study_researcher_roles)

    researchers: Dict[int, str] = field(default_factory=dict)
    selection: ResearcherViewModel = field(default_factory=ResearcherViewModel)

    def __post_init__(self):
        super().__init__()

    def to_study_researcher(self) -> StudyResearcher:
        return StudyResearcher(
            id=self.id,
            study_id=self.study_id,
            researcher_id=self.researcher_id,
            role=self.role,
            study_comments=self.study_comments,
            number=self.number,
            name=self.name,
            phone=self.phone,
            email=self.email,
        )

    def to_dict(self):
        return {
            "id": self.id,
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
        self.id = data.get("id", 0)
        self.study_id = data.get("study_id", 0)
        self.researcher_id = data.get("researcher_id", 0)
        self.role = data.get("role", "standard")
        self.study_comments = data.get("study_comments", "")
        self.number = data.get("number", "")
        self.name = data.get("name", "")
        self.phone = data.get("phone", "")
        self.email = data.get("email", "")
        
        self.selection.id = self.researcher_id
        self.selection.name = self.name
        self.selection.number = self.number
        self.selection.phone = self.phone
        self.selection.email = self.email

    async def save(self):
        sr = self.to_study_researcher()
        await sr.save()
        if sr.id:
            self.id = sr.id
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
                researcher = await Researcher.load(self.researcher_id)
                if researcher:
                    self.selection.copy(researcher)
                    self.number = researcher.number
                    self.name = researcher.name
                    self.phone = researcher.phone
                    self.email = researcher.email

        return None

    async def load_researchers(self):
        researcher_list = ResearcherList()
        await researcher_list.load()
        self.researchers = {r.id: r.name for r in researcher_list.researchers}