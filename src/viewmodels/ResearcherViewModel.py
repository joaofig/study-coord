
from nicegui import binding
from nicegui.observables import ObservableSet

from models import Researcher
from viewmodels.ViewModel import ViewModel


@binding.bindable_dataclass
class ResearcherViewModel(ViewModel):
    id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""
    data_changed: bool = False
    change_set = ObservableSet()
    is_old: bool = False

    def __post_init__(self):
        super().__init__()
        self.subscribe("researcher", "researcher_selected", self._handle_researcher_selected)

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_researcher_selected(self, **kwargs):
        researcher_row = kwargs.get("researcher")
        if researcher_row:
            researcher_id = researcher_row.get("id")
            if researcher_id:
                researcher = await Researcher.load(researcher_id=int(researcher_id))
                if researcher:
                    self.copy(researcher)

    async def _on_message(self, msg: str, **kwargs):
        match msg:
            case "copy":
                self.copy(kwargs.get("researcher"))

            case "save":
                await self.save()

            case "load":
                r = await Researcher.load(researcher_id=int(kwargs.get("researcher_id")))
                if r:
                    self.copy(r)
        return None

    def copy(self, researcher: Researcher):
        self.id = researcher.id
        self.name = researcher.name
        self.number = researcher.number
        self.phone = researcher.phone
        self.email = researcher.email
        self.comments = researcher.comments or ""
        self.data_changed = False
        self.is_old = researcher.id > 0
        self.change_set.clear()
        
    def to_researcher(self):
        return Researcher(
            id=self.id,
            number=self.number,
            name=self.name,
            phone=self.phone,
            email=self.email,
            comments=self.comments
        )

    async def save(self):
        researcher = self.to_researcher()
        await researcher.save()
        if researcher.id:
            self.id = researcher.id
        self.data_changed = False
        self.is_old = True
        await self.notify("researcher_saved", researcher=researcher)
