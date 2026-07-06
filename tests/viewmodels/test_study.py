from typing import List
from unittest.mock import AsyncMock, Mock, patch

import pytest
from nicegui import ui

from src.models.study import Study, StudyRow
from src.viewmodels.StudyViewModel import StudyViewModel
from src.viewmodels.StudyListViewModel import StudyListViewModel

EXISTING_STUDY_ID = 7
NEW_STUDY_ID = 23
SELECTED_STUDY_ID = 11
MISSING_STUDY_ID = 404
STUDY_NAME = "Cardio Trial"
EMPTY_STUDY_NAME = ""
STUDY_SPONSOR = "Acme Pharma"
STUDY_START_DATE = "2026-02-03"
STUDY_END_DATE = "2026-12-31"
STUDY_COMMENTS = "Follow up required"
PROTOCOL_VISITS = 4
EMPTY_ID = 0
NO_PATIENTS = 0
NO_VISITS = 0
NO_RESEARCHERS = 0
NO_ADVERSE_EVENTS = 0


def make_study(
    *,
    study_id: int | None = EXISTING_STUDY_ID,
    name: str = STUDY_NAME,
    sponsor: str = STUDY_SPONSOR,
    start_date: str = STUDY_START_DATE,
    end_date: str | None = STUDY_END_DATE,
    proto_visits: int = PROTOCOL_VISITS,
    comments: str | None = STUDY_COMMENTS,
) -> Study:
    return Study(
        id=study_id,
        name=name,
        sponsor=sponsor,
        start_date=start_date,
        end_date=end_date,
        proto_visits=proto_visits,
        comments=comments,
    )


def make_study_row(study_id: int = EXISTING_STUDY_ID) -> StudyRow:
    return StudyRow(
        id=study_id,
        name=STUDY_NAME,
        sponsor=STUDY_SPONSOR,
        start_date=STUDY_START_DATE,
        end_date=STUDY_END_DATE,
        proto_visits=PROTOCOL_VISITS,
        comments=STUDY_COMMENTS,
        patients=NO_PATIENTS,
        visits=NO_VISITS,
        researchers=NO_RESEARCHERS,
        adverse_events=NO_ADVERSE_EVENTS,
    )


@pytest.fixture
def fake_repository():
    class FakeStudyRepository:
        rows: List[StudyRow] = []
        studies_by_id: dict[int, dict] = {}
        requested_ids: List[int] = []
        saved_studies: List[dict] = []

        @classmethod
        async def list(cls) -> List[StudyRow]:
            return cls.rows

        @classmethod
        async def get(cls, study_id: int) -> dict | None:
            cls.requested_ids.append(study_id)
            return cls.studies_by_id.get(study_id)

        @classmethod
        async def save(cls, study: dict) -> dict:
            cls.saved_studies.append(study)
            if study.get("id") == EMPTY_ID or study.get("id") is None:
                study["id"] = NEW_STUDY_ID
            return study

    return FakeStudyRepository


def assert_view_model_matches_study(view_model: StudyViewModel, study: Study) -> None:
    assert view_model.id == (study.id or EMPTY_ID)
    assert view_model.name == study.name
    assert view_model.sponsor == study.sponsor
    assert view_model.visits == study.proto_visits
    assert view_model.start_date == study.start_date
    assert view_model.end_date == (study.end_date or "")
    assert view_model.comments == (study.comments or "")


def assert_studies_match(actual: Study, expected: Study) -> None:
    assert actual.id == expected.id
    assert actual.name == expected.name
    assert actual.sponsor == expected.sponsor
    assert actual.start_date == expected.start_date
    assert actual.end_date == expected.end_date
    assert actual.proto_visits == expected.proto_visits
    assert actual.comments == expected.comments


@pytest.mark.asyncio
async def test_study_view_model_copy_populates_editable_fields() -> None:
    view_model = StudyViewModel()
    study = make_study(end_date=None, comments=None)

    await view_model.copy(study)

    assert_view_model_matches_study(view_model, study)


def test_study_view_model_to_study_preserves_current_fields() -> None:
    view_model = StudyViewModel(
        id=EXISTING_STUDY_ID,
        name=STUDY_NAME,
        sponsor=STUDY_SPONSOR,
        visits=PROTOCOL_VISITS,
        start_date=STUDY_START_DATE,
        end_date=STUDY_END_DATE,
        comments=STUDY_COMMENTS,
    )

    study = view_model.to_study()

    assert_studies_match(study, make_study())


@pytest.mark.asyncio
async def test_save_persists_valid_study_updates_id_and_notifies(fake_repository) -> None:
    view_model = StudyViewModel(
        name=STUDY_NAME,
        sponsor=STUDY_SPONSOR,
        visits=PROTOCOL_VISITS,
        start_date=STUDY_START_DATE,
    )
    handler = AsyncMock()
    view_model.register(handler)

    with patch("src.models.study.StudyRepository", fake_repository):
        await view_model.save()

    assert view_model.id == NEW_STUDY_ID
    assert len(fake_repository.saved_studies) == 1
    saved_study = fake_repository.saved_studies[0]
    assert saved_study["name"] == STUDY_NAME
    assert saved_study["sponsor"] == STUDY_SPONSOR
    assert saved_study["proto_visits"] == PROTOCOL_VISITS
    handler.assert_awaited_once_with("study_saved", {})


@pytest.mark.asyncio
async def test_save_rejects_invalid_study_without_persisting(fake_repository) -> None:
    view_model = StudyViewModel(
        name=EMPTY_STUDY_NAME,
        sponsor=STUDY_SPONSOR,
        visits=PROTOCOL_VISITS,
        start_date=STUDY_START_DATE,
    )
    handler = AsyncMock()
    view_model.register(handler)

    with patch("src.models.study.StudyRepository", fake_repository), patch.object(ui, "notify") as notify:
        await view_model.save()

    assert fake_repository.saved_studies == []
    handler.assert_not_awaited()
    notify.assert_called_once()
    notification = notify.call_args.args[0]
    assert "Study name is required." in notification
    assert notify.call_args.kwargs["color"] == "negative"


@pytest.mark.asyncio
async def test_message_load_study_copies_repository_result(fake_repository) -> None:
    study = make_study()
    fake_repository.studies_by_id[EXISTING_STUDY_ID] = study.to_dict()
    view_model = StudyViewModel()

    with patch("src.models.study.StudyRepository", fake_repository):
        await view_model.call("load_study", str(EXISTING_STUDY_ID))

    assert fake_repository.requested_ids == [EXISTING_STUDY_ID]
    assert_view_model_matches_study(view_model, study)


@pytest.mark.asyncio
async def test_message_load_study_keeps_state_when_missing(fake_repository) -> None:
    view_model = StudyViewModel(name=STUDY_NAME)

    with patch("src.models.study.StudyRepository", fake_repository):
        await view_model.call("load_study", MISSING_STUDY_ID)

    assert fake_repository.requested_ids == [MISSING_STUDY_ID]
    assert view_model.name == STUDY_NAME


@pytest.mark.asyncio
async def test_message_save_study_delegates_to_save() -> None:
    view_model = StudyViewModel()
    view_model.save = AsyncMock()

    await view_model.call("save_study")

    view_model.save.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_study_list_load_replaces_rows_and_notifies(fake_repository) -> None:
    rows = [make_study_row(EXISTING_STUDY_ID), make_study_row(SELECTED_STUDY_ID)]
    fake_repository.rows = rows
    view_model = StudyListViewModel(StudyViewModel())
    handler = AsyncMock()
    view_model.register(handler)

    with patch("src.viewmodels.study.StudyRepository", fake_repository):
        await view_model.load()

    assert view_model.studies == rows
    handler.assert_awaited_once_with("list_changed", {})


@pytest.mark.asyncio
async def test_study_list_reloads_after_study_saved() -> None:
    view_model = StudyListViewModel(StudyViewModel())
    view_model.load = AsyncMock()

    await view_model.call("study_saved")

    view_model.load.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_study_list_loads_selected_study_into_child_view_model() -> None:
    child_view_model = Mock()
    child_view_model.message = AsyncMock()
    view_model = StudyListViewModel(child_view_model)

    await view_model.call("study_selected", {"id": SELECTED_STUDY_ID})

    child_view_model.message.assert_awaited_once_with("load_study", SELECTED_STUDY_ID)
