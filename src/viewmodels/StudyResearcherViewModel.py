from nicegui import binding

from models.researcher import StudyResearcher
from tools.messenger import send_message
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

    def __post_init__(self):
        super().__init__()

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
        await send_message("study_researcher_list", "load")
        self.changed = False

    async def handle_command(self, msg: str, **kwargs):
        match msg:
            case "save":
                return await self.save()
        return None
