from dataclasses import field
from typing import List, Dict

from nicegui import binding
from nicegui.binding import bind

from models.researcher import StudyResearcher, Researcher, ResearcherList
from tools.tasks import ManagedTasks
from viewmodels import ResearcherViewModel
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class StudyResearcherViewModel(ViewModel):
    id: int = 0
    study_id: int = 0
    researcher_id: int = 0
    role: str = "standard"
    study_comments: str = ""
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    changed: bool = False

    researchers: Dict[int, str] = field(default_factory=dict)
    selection = ResearcherViewModel()
    _id: int = 0

    def __post_init__(self):
        super().__init__()
        ManagedTasks().create(self._load_researchers)

        bind(self, "researcher_id", self, "_id", forward=self._on_researcher_id)

    async def _on_researcher_id(self, value):
        researcher = await Researcher.load(value)
        if researcher:
            self.selection.copy(researcher)

    def copy(self, researcher: StudyResearcher):
        self.id = researcher.id
        self.study_id = researcher.study_id
        self.researcher_id = researcher.researcher_id
        self.role = researcher.role
        self.study_comments = researcher.study_comments
        self.number = researcher.number
        self.name = researcher.name
        self.phone = researcher.phone
        self.email = researcher.email

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

    def from_dict(self, researcher: dict):
        self.id = researcher["id"]
        self.study_id = researcher["study_id"]
        self.researcher_id = researcher["researcher_id"]
        self.role = researcher["role"]
        self.study_comments = researcher["study_comments"]
        self.number = researcher["number"]
        self.name = researcher["name"]
        self.phone = researcher["phone"]
        self.email = researcher["email"]

    async def save(self):
        sr = self.to_study_researcher()
        await sr.save()
        if sr.id:
            self.id = sr.id
        await self.notify("study_researcher_saved")
        await self.broadcast("study_researcher_list", "load")
        self.changed = False

    async def _on_message(self, msg: str, **kwargs):
        """
        Handle incoming messages from the attached View.

        :param msg: The message to handle.
        :param kwargs: Additional keyword arguments.
        :return: None
        """
        match msg:
            case "save":
                return await self.save()
        return None

    async def _load_researchers(self):
        researcher_list = ResearcherList()
        await researcher_list.load()
        self.researchers = {r.id: r.name for r in researcher_list.researchers}
        await self.notify("researcher_list_loaded")