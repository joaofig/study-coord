from pydantic import BaseModel

from src.dtos.study import StudyDTO


class ResearcherDTO(BaseModel):
    id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""
    # study_count: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> ResearcherDTO:
        return ResearcherDTO(
            id=data.get("id", 0),
            number=data.get("number", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            comments=data.get("comments", ""),
            # study_count=data.get("study_count", 0),
        )

    def to_dict(self) -> dict:
        return self.model_dump()


class StudyResearcherDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    researcher_id: int = 0
    role: str = ""
    study_comments: str = ""

    study: StudyDTO | None = None
    researcher: ResearcherDTO | None = None

    @classmethod
    def from_dict(cls, data: dict) -> StudyResearcherDTO:
        return StudyResearcherDTO(
            id=data.get("id", 0),
            study_id=data.get("study_id", 0),
            researcher_id=data.get("researcher_id", 0),
            role=data.get("role", ""),
            study_comments=data.get("study_comments", ""),
        )

    def to_dict(self) -> dict:
        return self.model_dump()
