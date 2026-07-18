from pydantic import BaseModel


class ResearcherDTO(BaseModel):
    id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""
    study_count: int = 0

    def to_dict(self) -> dict:
        return self.model_dump()


class StudyResearcherDTO(BaseModel):
    id: int = 0
    researcher_id: int = 0
    study_id: int = 0
    role: str = ""
    study_comments: str = ""
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()
