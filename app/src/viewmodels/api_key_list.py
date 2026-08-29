from typing import Any

from src.models.api_key import ApiKeyModel
from nicemvvm.tools.observability import GridList
from src.viewmodels import ViewModel


class ApiKeyListViewModel(ViewModel):
    selected_id: int = 0

    def __init__(self):
        super().__init__()

        self.api_keys = GridList()
        self.model = ApiKeyModel()

    async def _load(self, **kwargs):
        if "user_name" in kwargs:
            api_keys = await self.model.list(kwargs["user_name"])
            self.api_keys.replace([s.to_dict() for s in api_keys])
        else:
            self.api_keys.replace([])

    async def _on_call(self, msg: str, **kwargs) -> Any:
        match msg:
            case "load":
                await self._load()

            case "delete":
                api_key_id = kwargs["api_key_id"]
                await self.model.delete(api_key_id)
                await self._load()
                await self.broadcast(
                    "api_kay", message="deleted", api_key_id=api_key_id
                )

            case "select":
                self.selected_id = kwargs.get("api_key_id", 0)
                if self.selected_id:
                    await self.broadcast(
                        "api_key", message="selected", api_key_id=self.selected_id
                    )
        return None
