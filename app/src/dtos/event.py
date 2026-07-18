from pydantic import BaseModel


class EventDTO(BaseModel):
    id: int = 0
    study_id: int = 0
    patient_id: int = 0
    date: str = ""
    event_type: str = ""
    description: str = ""
    comments: str = ""
    patient_number: str = ""
    patient_name: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()
