from typing import Annotated

from fastapi import Header
from nicegui import app

from src.repositories import StudyRepository, PatientRepository, VisitRepository


async def validate_api_key(x_api_key: str | None):
    if x_api_key != "my-secret-key":
        return {"error": "Invalid API key"}
    return None


@app.get('/studies')
async def get_studies(x_api_key: Annotated[str | None, Header()] = None):
    repo = StudyRepository()
    return {'studies': await repo.list()}


@app.get('/studies/{study_id}')
async def get_study(study_id: int,
                    x_api_key: Annotated[str | None, Header()] = None):
    repo = StudyRepository()
    study = await repo.load(study_id)
    if study is None:
        return {"error": "Study not found"}
    return {'study': study}


@app.get('/studies/{study_id}/patients')
async def get_subjects(study_id: int,
                       x_api_key: Annotated[str | None, Header()] = None):
    repo = PatientRepository()
    return {"patients": await repo.list(study_id)}


@app.get('/studies/{study_id}/patients/{patient_id}')
async def get_subject(study_id: int, patient_id: int,
                      x_api_key: Annotated[str | None, Header()] = None):
    repo = PatientRepository()
    patient = await repo.load(patient_id)
    if patient is None:
        return {"error": "Patient not found"}
    if patient.study_id != study_id:
        return {"error": "Patient does not belong to the study"}
    return {"patient": patient}


@app.get("/studies/{study_id}/patients/{patient_id}/visits")
async def get_visits(study_id: int, patient_id: int,
                     x_api_key: Annotated[str | None, Header()] = None):
    repo = VisitRepository()
    return {'visits': await repo.list(study_id=study_id, patient_id=patient_id)}


@app.get("/studies/{study_id}/patients/{patient_id}/visits/{visit_id}")
async def get_visits(study_id: int, patient_id: int, visit_id: int,
                     x_api_key: Annotated[str | None, Header()] = None):
    repo = VisitRepository()
    visit = await repo.load(visit_id)
    if visit is None:
        return {"error": "Visit not found"}
    if visit.patient_id != patient_id:
        return {"error": "Visit does not belong to the patient"}

    study_repo = StudyRepository()
    study = await study_repo.load(study_id)
    if study is None:
        return {"error": "Study not found"}
    if study.study_id != visit.study_id:
        return {"error": "Visit does not belong to the study"}
    return {"visit": visit}
