import pytest
from datetime import date
from unittest.mock import AsyncMock, patch
from src.dtos.adverse_event import AdverseEventDTO
from src.viewmodels.adverse_event import AdverseEventViewModel
from src.viewmodels.adverse_event_list import AdverseEventListViewModel

@pytest.mark.asyncio
async def test_adverse_event_view_model_save():
    # Setup
    vm = AdverseEventViewModel()
    vm.study_id = 1
    vm.patient_id = 101
    vm.event_type = "Severe"
    vm.description = "Test Event"
    
    with patch("src.models.adverse_event.AdverseEventModel.repo") as mock_repo:
        mock_repo.save = AsyncMock(return_value={"adverse_event_id": 301})
        
        # Action
        await vm.save()
        
        # Verify
        assert vm.adverse_event_id == 301
        mock_repo.save.assert_called_once()
        args = mock_repo.save.call_args[0][0]
        assert args.event_type == "Severe"
        assert args.description == "Test Event"

@pytest.mark.asyncio
async def test_adverse_event_view_model_load():
    # Setup
    vm = AdverseEventViewModel()
    mock_dto = AdverseEventDTO(
        adverse_event_id=301,
        study_id=1,
        patient_id=101,
        event_date=date(2024, 1, 1),
        event_type="Mild",
        description="Headache"
    )
    
    with patch("src.models.adverse_event.AdverseEventModel.load", new_callable=AsyncMock, return_value=mock_dto), \
         patch("src.models.patient.PatientModel.load", new_callable=AsyncMock, return_value=None):
        # Action
        await vm.load(301)
        
        # Verify
        assert vm.adverse_event_id == 301
        assert vm.event_type == "Mild"
        assert vm.description == "Headache"

@pytest.mark.asyncio
async def test_adverse_event_list_view_model_load():
    # Setup
    vm = AdverseEventListViewModel()
    mock_events = [
        AdverseEventDTO(adverse_event_id=1, study_id=1, patient_id=101, event_type="E1"),
        AdverseEventDTO(adverse_event_id=2, study_id=1, patient_id=101, event_type="E2"),
    ]
    
    with patch("src.models.adverse_event.AdverseEventModel.list", new_callable=AsyncMock, return_value=mock_events):
        # Action
        await vm.call("load", study_id=1, adverse_event_id=101)
        
        # Verify
        assert len(vm.events) == 2
        assert vm.study_id == 1
        assert vm.adverse_event_id == 101
        assert vm.events[0].event_type == "E1"
