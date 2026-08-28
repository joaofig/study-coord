from typing import Annotated

from fastapi import Header
from nicegui import app
from src.dtos.user import hash_password
from src.repositories import (
    ApiKeyRepository,
    PatientRepository,
    StudyRepository,
    VisitRepository,
)

INVALID_API_KEY = "Invalid API key"


async def validate_api_key(x_api_key: str | None) -> bool:
    api_key_hash = hash_password(x_api_key) if x_api_key else None
    if api_key_hash is not None:
        repo = ApiKeyRepository()
        api_key_dto = await repo.find_by_key(api_key_hash)
        return api_key_dto is not None
    return False


@app.get("/studies")
async def get_studies(x_api_key: Annotated[str | None, Header()] = None):
    if not await validate_api_key(x_api_key):
        return {"error": INVALID_API_KEY}
    repo = StudyRepository()
    return {"studies": await repo.list()}


@app.get("/studies/{study_id}")
async def get_study(study_id: int, x_api_key: Annotated[str | None, Header()] = None):
    if not await validate_api_key(x_api_key):
        return {"error": INVALID_API_KEY}
    repo = StudyRepository()
    study = await repo.load(study_id)
    if study is None:
        return {"error": "Study not found"}
    return {"study": study}


@app.get("/studies/{study_id}/patients")
async def get_subjects(
    study_id: int, x_api_key: Annotated[str | None, Header()] = None
):
    if not await validate_api_key(x_api_key):
        return {"error": INVALID_API_KEY}
    repo = PatientRepository()
    return {"patients": await repo.list(study_id)}


@app.get("/studies/{study_id}/patients/{patient_id}")
async def get_subject(
    study_id: int, patient_id: int, x_api_key: Annotated[str | None, Header()] = None
):
    if not await validate_api_key(x_api_key):
        return {"error": INVALID_API_KEY}
    repo = PatientRepository()
    patient = await repo.load(patient_id)
    if patient is None:
        return {"error": "Patient not found"}
    if patient.study_id != study_id:
        return {"error": "Patient does not belong to the study"}
    return {"patient": patient}


@app.get("/studies/{study_id}/patients/{patient_id}/visits")
async def get_visits(
    study_id: int, patient_id: int, x_api_key: Annotated[str | None, Header()] = None
):
    if not await validate_api_key(x_api_key):
        return {"error": INVALID_API_KEY}
    repo = VisitRepository()
    return {"visits": await repo.list(study_id=study_id, patient_id=patient_id)}


@app.get("/studies/{study_id}/patients/{patient_id}/visits/{visit_id}")
async def get_visits(
    study_id: int,
    patient_id: int,
    visit_id: int,
    x_api_key: Annotated[str | None, Header()] = None,
):
    if not await validate_api_key(x_api_key):
        return {"error": INVALID_API_KEY}
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
