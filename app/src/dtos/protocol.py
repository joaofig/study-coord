from pydantic import BaseModel


class ProtocolDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    title: str = ""
    date: str = ""
    description: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()
