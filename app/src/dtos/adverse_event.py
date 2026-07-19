from pydantic import BaseModel


class AdverseEventDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    patient_id: int = 0
    event_date: str = ""
    event_type: str = ""
    description: str = ""
    comments: str = ""
    patient_number: str = ""
    patient_name: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()
