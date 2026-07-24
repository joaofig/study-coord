import pytest
from unittest.mock import AsyncMock, patch
from src.dtos.researcher import ResearcherDTO
from src.viewmodels.researcher import ResearcherViewModel
from src.viewmodels.researcher_list import ResearcherListViewModel

@pytest.mark.asyncio
async def test_researcher_view_model_save():
    # Setup
    vm = ResearcherViewModel()
    vm.name = "John Doe"
    vm.number = "R001"
    vm.phone = "123456"
    vm.email = "john@example.com"
    
    with patch("src.models.researcher.ResearcherModel.repo") as mock_repo:
        mock_repo.save = AsyncMock(return_value={"researcher_id": 123})
        
        # Action
        await vm.save()
        
        # Verify
        assert vm.researcher_id == 123
        mock_repo.save.assert_called_once()
        args = mock_repo.save.call_args[0][0]
        assert args.name == "John Doe"
        assert args.number == "R001"

@pytest.mark.asyncio
async def test_researcher_view_model_load():
    # Setup
    vm = ResearcherViewModel()
    mock_dto = ResearcherDTO(
        researcher_id=123,
        name="Jane Doe",
        number="R002",
        phone="654321",
        email="jane@example.com",
        comments="Some comments"
    )
    
    with patch("src.models.researcher.ResearcherModel.load", new_callable=AsyncMock, return_value=mock_dto):
        # Action
        await vm.call("load", researcher_id=123)
        
        # Verify
        assert vm.researcher_id == 123
        assert vm.name == "Jane Doe"
        assert vm.number == "R002"
        assert vm.comments == "Some comments"

@pytest.mark.asyncio
async def test_researcher_list_view_model_load():
    # Setup
    vm = ResearcherListViewModel()
    mock_researchers = [
        ResearcherDTO(researcher_id=1, name="R1", number="N1"),
        ResearcherDTO(researcher_id=2, name="R2", number="N2"),
    ]
    
    with patch("src.models.researcher.ResearcherModel.list", new_callable=AsyncMock, return_value=mock_researchers):
        # Action
        await vm.load()
        
        # Verify
        assert len(vm.researchers) == 2
        assert vm.researchers[0].name == "R1"
        assert vm.researchers[1].name == "R2"

@pytest.mark.asyncio
async def test_researcher_list_view_model_delete():
    # Setup
    vm = ResearcherListViewModel()
    
    with patch("src.models.researcher.ResearcherModel.delete", new_callable=AsyncMock) as mock_delete, \
         patch("src.models.researcher.ResearcherModel.list", new_callable=AsyncMock, return_value=[]):
        # Action
        await vm.call("delete", researcher_id=123)
        
        # Verify
        mock_delete.assert_called_once_with(researcher_id=123)
