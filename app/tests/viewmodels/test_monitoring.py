import pytest
from unittest.mock import AsyncMock, patch
from viewmodels.MonitoringViewModel import MonitoringViewModel
from viewmodels.MonitoringListViewModel import MonitoringListViewModel


@pytest.mark.asyncio
async def test_monitoring_view_model_save():
    view_model = MonitoringViewModel(
        study_id=1,
        date="2024-07-07",
        monitor="John Doe",
        comments="Routine check"
    )
    
    with patch("src.models.monitoring.MonitoringRepository") as mock_repo_class:
        mock_repo = mock_repo_class.return_value
        mock_repo.save = AsyncMock(return_value={"id": 123})
        
        await view_model.save()
        
        assert view_model.id == 123
        mock_repo.save.assert_called_once()
        args = mock_repo.save.call_args[0][0]
        assert args["study_id"] == 1
        assert args["date"] == "2024-07-07"
        assert args["monitor"] == "John Doe"

@pytest.mark.asyncio
async def test_monitoring_list_view_model_load():
    view_model = MonitoringListViewModel()
    
    mock_data = [
        {"id": 1, "study_id": 1, "date": "2024-01-01", "monitor": "M1", "comments": "C1"},
        {"id": 2, "study_id": 1, "date": "2024-02-01", "monitor": "M2", "comments": "C2"},
    ]
    
    with patch("src.db.repository.MonitoringRepository.MonitoringRepository.get_by_study_id", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_data
        
        await view_model._load_monitoring(1)
        
        assert len(view_model.monitoring_visits) == 2
        assert view_model.monitoring_visits[0]["monitor"] == "M1"
        assert view_model.monitoring_visits[1]["monitor"] == "M2"
