from pydantic import BaseModel


class ResearcherDTO(BaseModel):
    id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""
    study_count: int = 0