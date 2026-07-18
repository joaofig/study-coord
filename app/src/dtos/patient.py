from pydantic import BaseModel


class PatientDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    number: str = ""
    name: str = ""
    start_date: str = ""
    exit_date: str = ""
    status: str = "active"
    comments: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()