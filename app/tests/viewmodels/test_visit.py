import pytest
from datetime import date
from unittest.mock import AsyncMock, patch
from src.dtos.visit import VisitDTO
from src.viewmodels.visit import VisitViewModel
from src.viewmodels.visit_list import VisitListViewModel

@pytest.mark.asyncio
async def test_visit_view_model_save():
    # Setup
    vm = VisitViewModel()
    vm.study_id = 1
    vm.patient_id = 101
    vm.visit_type = "Screening"
    
    with patch("src.models.visit.VisitModel.repo") as mock_repo:
        mock_repo.save = AsyncMock(return_value={"visit_id": 201})
        
        # Action
        await vm.save()
        
        # Verify
        assert vm.visit_id == 201
        mock_repo.save.assert_called_once()
        args = mock_repo.save.call_args[0][0]
        assert args.visit_type == "Screening"
        assert args.patient_id == 101

@pytest.mark.asyncio
async def test_visit_view_model_load():
    # Setup
    vm = VisitViewModel()
    mock_dto = VisitDTO(
        visit_id=201,
        study_id=1,
        patient_id=101,
        visit_date=date(2024, 1, 1),
        visit_type="Follow-up"
    )
    
    with patch("src.models.visit.VisitModel.load", new_callable=AsyncMock, return_value=mock_dto):
        # Action
        await vm.load(201)
        
        # Verify
        assert vm.visit_id == 201
        assert vm.visit_type == "Follow-up"

@pytest.mark.asyncio
async def test_visit_list_view_model_load():
    # Setup
    vm = VisitListViewModel()
    mock_visits = [
        VisitDTO(visit_id=1, study_id=1, patient_id=101, visit_type="V1"),
        VisitDTO(visit_id=2, study_id=1, patient_id=101, visit_type="V2"),
    ]
    
    with patch("src.models.visit.VisitModel.list", new_callable=AsyncMock, return_value=mock_visits):
        # Action
        await vm.call("load", study_id=1)
        
        # Verify
        assert len(vm.visits) == 2
        assert vm.study_id == 1
        assert vm.visits[0]["visit_type"] == "V1"
