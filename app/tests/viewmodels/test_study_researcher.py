import pytest
from unittest.mock import AsyncMock, patch
from src.viewmodels.study_researcher import StudyResearcherViewModel
from src.viewmodels.study_researcher_list import StudyResearcherListViewModel
from src.dtos.researcher import ResearcherDTO as Researcher, StudyResearcherDTO


@pytest.mark.asyncio
async def test_study_researcher_view_model_load_updates_fields():
    # Setup
    researcher_id = 1
    researcher = Researcher(
        researcher_id=researcher_id,
        number="R001",
        name="John Doe",
        phone="123",
        email="john@example.com",
    )
    sr_dto = StudyResearcherDTO(researcher_id=researcher_id, researcher=researcher)

    with patch(
        "src.models.study_researcher.StudyResearcherModel.load",
        new_callable=AsyncMock,
        return_value=sr_dto,
    ):
        vm = StudyResearcherViewModel()
        vm.researcher_id = researcher_id

        # Action
        await vm.call("load")

        # Verify
        assert vm.selection.researcher_id == researcher_id
        assert vm.selection.name == "John Doe"
        assert vm.number == "R001"
        assert vm.name == "John Doe"


@pytest.mark.asyncio
async def test_study_researcher_view_model_from_dict():
    # Setup
    data = {
        "id": 10,
        "study_id": 100,
        "researcher_id": 1,
        "role": "principal",
        "study_comments": "Test comments",
        "number": "R001",
        "name": "John Doe",
        "phone": "123",
        "email": "john@example.com",
    }
    vm = StudyResearcherViewModel()

    # Action
    vm.from_dict(data)

    # Verify
    assert vm.sr_id == 10
    assert vm.study_id == 100
    assert vm.role == "principal"
    assert vm.selection.name == "John Doe"
    assert vm.name == "John Doe"


@pytest.mark.asyncio
async def test_study_researcher_view_model_save():
    # Setup
    vm = StudyResearcherViewModel()
    vm.study_id = 100
    vm.researcher_id = 1
    vm.role = "principal"

    with patch(
        "src.models.study_researcher.StudyResearcherModel.save", new_callable=AsyncMock
    ) as mock_save:
        # Action
        await vm.call("save")

        # Verify
        mock_save.assert_called_once()


@pytest.mark.asyncio
async def test_study_researcher_list_view_model_load():
    # Setup
    vm = StudyResearcherListViewModel()
    vm.study_id = 1
    mock_researchers = [
        StudyResearcherDTO(sr_id=1, study_id=1, researcher_id=10),
        StudyResearcherDTO(sr_id=2, study_id=1, researcher_id=11),
    ]

    with patch(
        "src.models.study_researcher.StudyResearcherModel.list",
        new_callable=AsyncMock,
        return_value=mock_researchers,
    ):
        # Action
        await vm.load()

        # Verify
        assert len(vm.researchers) == 2
        assert vm.researchers[0].sr_id == 1


@pytest.mark.asyncio
async def test_study_researcher_list_view_model_saved_message():
    # Setup
    vm = StudyResearcherListViewModel()
    vm.study_id = 1

    with patch(
        "src.models.study_researcher.StudyResearcherModel.list",
        new_callable=AsyncMock,
        return_value=[],
    ) as mock_list:
        # Action
        await vm.call("study_researcher_saved")

        # Verify
        mock_list.assert_called_once_with(1)
