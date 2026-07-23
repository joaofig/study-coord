

from dtos.base import BaseDTO
from src.dtos.study import StudyDTO
from src.tools.user import dict_to_datetime


class ResearcherDTO(BaseDTO):
    researcher_id: int = 0
    number: str = ""
    name: str = ""
    phone: str = ""
    email: str = ""
    comments: str = ""

    # study_count: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> ResearcherDTO:
        return ResearcherDTO(
            researcher_id=data.get("researcher_id", 0),
            number=data.get("number", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            comments=data.get("comments", ""),
            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", ""),
            # study_count=data.get("study_count", 0),
        )

    def to_dict(self) -> dict:
        return {
            "researcher_id": self.researcher_id,
            "number": self.number,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "comments": self.comments,
        } | super().to_dict()


class StudyResearcherDTO(BaseDTO):
    sr_id: int = 0
    study_id: int = 0
    researcher_id: int = 0
    role: str = ""
    study_comments: str = ""

    study: StudyDTO | None = None
    researcher: ResearcherDTO | None = None

    @classmethod
    def from_dict(cls, data: dict) -> StudyResearcherDTO:
        return StudyResearcherDTO(
            sr_id=data.get("sr_id", 0),
            study_id=data.get("study_id", 0),
            researcher_id=data.get("researcher_id", 0),
            role=data.get("role", ""),
            study_comments=data.get("study_comments", ""),

            created_at=dict_to_datetime(data, "created_at"),
            created_by=data.get("created_by", ""),
            updated_at=dict_to_datetime(data, "updated_at"),
            updated_by=data.get("updated_by", "")
        )

    def to_dict(self) -> dict:
        return {
            "sr_id": self.sr_id,
            "study_id": self.study_id,
            "researcher_id": self.researcher_id,
            "role": self.role,
            "study_comments": self.study_comments,
        } | super().to_dict()
