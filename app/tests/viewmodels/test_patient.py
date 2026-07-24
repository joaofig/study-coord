import pytest
from datetime import date
from unittest.mock import AsyncMock, patch
from src.dtos.patient import PatientDTO
from src.viewmodels.patient import PatientViewModel
from src.viewmodels.patient_list import PatientListViewModel

@pytest.mark.asyncio
async def test_patient_view_model_save():
    # Setup
    vm = PatientViewModel()
    vm.study_id = 1
    vm.name = "Patient One"
    vm.number = "P001"
    
    with patch("src.models.patient.PatientModel.repo") as mock_repo:
        mock_repo.save = AsyncMock(return_value={"patient_id": 101})
        
        # Action
        await vm.save()
        
        # Verify
        assert vm.patient_id == 101
        mock_repo.save.assert_called_once()
        args = mock_repo.save.call_args[0][0]
        assert args.name == "Patient One"
        assert args.study_id == 1

@pytest.mark.asyncio
async def test_patient_view_model_from_dict():
    # Setup
    vm = PatientViewModel()
    data = {
        "patient_id": 101,
        "study_id": 1,
        "number": "P001",
        "name": "Patient One",
        "start_date": "2024-01-01",
        "exit_date": None,
        "status": "active",
        "comments": "No comments",
        "created_at": "2024-01-01T00:00:00",
        "created_by": "admin",
        "updated_at": "2024-01-01T00:00:00",
        "updated_by": "admin"
    }
    
    # Action
    vm.from_dict(data)
    
    # Verify
    assert vm.patient_id == 101
    assert vm.name == "Patient One"
    assert vm.start_date == date(2024, 1, 1)

@pytest.mark.asyncio
async def test_patient_list_view_model_load():
    # Setup
    vm = PatientListViewModel()
    mock_patients = [
        PatientDTO(patient_id=1, study_id=1, name="P1", number="N1"),
        PatientDTO(patient_id=2, study_id=1, name="P2", number="N2"),
    ]
    
    with patch("src.models.patient.PatientModel.list", new_callable=AsyncMock, return_value=mock_patients):
        # Action
        await vm.call("load", study_id=1)
        
        # Verify
        assert len(vm.patients) == 2
        assert vm.study_id == 1
        assert vm.patients[0].name == "P1"

@pytest.mark.asyncio
async def test_patient_list_view_model_delete():
    # Setup
    vm = PatientListViewModel()
    vm.study_id = 1
    
    with patch("src.models.patient.PatientModel.delete", new_callable=AsyncMock) as mock_delete, \
         patch("src.models.patient.PatientModel.list", new_callable=AsyncMock, return_value=[]):
        # Action
        await vm.call("delete_patient", patient_id=101)
        
        # Verify
        mock_delete.assert_called_once_with(101)
