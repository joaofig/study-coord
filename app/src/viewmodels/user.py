import hashlib
from datetime import date
from typing import Any

from nicegui import binding
from nicegui.observables import ObservableSet

from src.dtos.user import UserDTO
from src.models import UserModel
from src.viewmodels.view_model import ViewModel


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@binding.bindable_dataclass
class UserViewModel(ViewModel):
    user_id: int = 0
    user_name: str = ""
    pass_hash: str = ""
    role: str = "User"
    created_at: date = date.today()
    created_by: str = ""
    updated_at: date = date.today()
    updated_by: str = ""
    data_changed: bool = False
    change_set = ObservableSet()
    is_old: bool = False
    model: UserModel = UserModel()

    password_1: str = ""
    password_2: str = ""

    def __post_init__(self):
        super().__init__()
        self.subscribe("user", "user_selected", self._handle_user_selected)

    def _field_changed(self, field_name: str):
        self.changed = True
        self.change_set.add(field_name)

    async def _handle_user_selected(self, **kwargs):
        user_row = kwargs.get("user")
        if user_row:
            user_id = user_row.get("user_id")
            if user_id:
                user = await self.model.load(user_id=int(user_id))
                if user:
                    self.copy(user)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "copy":
                self.copy(kwargs.get("user"))

            case "save":
                await self.save()

            case "load":
                if "user_id" in kwargs:
                    u = await self.model.load(user_id=int(kwargs.get("user_id")))
                    if u:
                        self.copy(u)
        return None

    def copy(self, user: UserDTO):
        self.user_id = user.user_id
        self.user_name = user.user_name
        self.pass_hash = user.pass_hash
        self.role = user.role
        self.created_at = user.created_at
        self.created_by = user.created_by
        self.updated_at = user.updated_at
        self.updated_by = user.updated_by
        self.data_changed = False
        self.is_old = user.user_id > 0
        self.change_set.clear()
        
    def to_dto(self) -> UserDTO:
        return UserDTO(
            user_id=self.user_id,
            user_name=self.user_name,
            pass_hash=self.pass_hash,
            role=self.role,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by
        )

    async def save(self):
        self.pass_hash = hash_password(self.password_1)
        user = self.to_dto()
        await self.model.save(user)
        if user.user_id:
            self.user_id = user.user_id
        self.data_changed = False
        self.is_old = True
