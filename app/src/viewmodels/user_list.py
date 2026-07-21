from typing import Any

from nicegui.observables import ObservableList

from src.models import UserModel
from src.viewmodels.view_model import ViewModel


class UserListViewModel(ViewModel):
    users = ObservableList()
    selected_id: int = 0
    model: UserModel = UserModel()

    def __init__(self):
        super().__init__()
        self.subscribe(channel="user_list",
                       message="load",
                       handler=self._on_load)

    async def load(self):
        self.users.clear()
        users = await self.model.list()
        print(users)
        self.users.extend(users)

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self.load()

            case "user_selected":
                if "user_id" in kwargs:
                    self.selected_id = int(str(kwargs["user_id"]))

            case "delete":
                user_id = kwargs.get("user_id")
                if user_id:
                    await self.model.delete(user_id=int(str(user_id)))
                await self.load()
                # await self.broadcast("user_list", "load")
        return None

    async def _on_load(self, **kwargs):
        await self.load()
