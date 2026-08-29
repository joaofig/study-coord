from datetime import datetime
from typing import Any

from nicegui import binding
from src.dtos.user import UserDTO, hash_password
from src.models.user import UserModel
from nicemvvm.tools.user import get_user_name
from src.viewmodels.view_model import ViewModel


@binding.bindable_dataclass
class UserViewModel(ViewModel):
    user_id: int = 0
    user_name: str = ""
    pass_hash: str = ""
    user_role: str = "User"
    change_pass: bool = False
    created_at: datetime = datetime.now()
    created_by: str = ""
    updated_at: datetime = datetime.now()
    updated_by: str = ""

    password_1: str = ""
    password_2: str = ""

    def __post_init__(self):
        super().__init__()

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "copy":
                self.copy(kwargs.get("user"))

            case "save":
                await self.save()

            case "load":
                if "user_id" in kwargs:
                    model: UserModel = UserModel()
                    u = await model.load(user_id=kwargs.get("user_id", 0))
                    if u:
                        self.copy(u)
        return None

    def copy(self, user: UserDTO):
        self.user_id = user.user_id
        self.user_name = user.user_name
        self.pass_hash = user.pass_hash
        self.user_role = user.user_role
        self.change_pass = user.change_pass
        self.created_at = user.created_at
        self.created_by = user.created_by
        self.updated_at = user.updated_at
        self.updated_by = user.updated_by

    def to_dto(self) -> UserDTO:
        is_old = self.user_id > 0
        return UserDTO(
            user_id=self.user_id,
            user_name=self.user_name,
            pass_hash=self.pass_hash,
            user_role=self.user_role,
            created_at=self.created_at if is_old else datetime.now(),
            created_by=self.created_by if is_old else get_user_name(),
            updated_at=datetime.now(),
            updated_by=get_user_name(),
            change_pass=self.change_pass,
        )

    async def save(self):
        self.pass_hash = hash_password(self.password_1)
        user = self.to_dto()
        user.log_change(self.user_id)
        model: UserModel = UserModel()
        await model.save(user)
        if user.user_id:
            self.user_id = user.user_id
