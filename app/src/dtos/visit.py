from pydantic import BaseModel


class Visit(BaseModel):
    id: int                         # Read-only unique identifier for the visit
    study_id: int                   # Identifier for the study associated with the visit
    patient_id: int                 # Identifier for the patient associated with the visit
    visit_date: str                 # Date of the visit
    visit_type: str = "visit"       # Type of the visit
    comments: str = ""              # Additional comments about the visit
    patient_number: str = ""
    patient_name: str = ""

    def to_dict(self) -> dict:
        return self.model_dump()
