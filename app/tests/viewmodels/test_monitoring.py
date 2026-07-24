import pytest
from unittest.mock import AsyncMock, patch
from src.dtos.monitoring import MonitoringDTO
from src.viewmodels.monitoring import MonitoringViewModel
from src.viewmodels.monitoring_list import MonitoringListViewModel


@pytest.mark.asyncio
async def test_monitoring_view_model_save():
    view_model = MonitoringViewModel(
        study_id=1,
        meeting_date="2024-07-07",
        monitor="John Doe",
        comments="Routine check",
    )

    with patch("src.models.monitoring.MonitoringModel.repo") as mock_repo:
        mock_repo.save = AsyncMock(return_value={"monitoring_id": 123})

        await view_model.save()

        assert view_model.monitoring_id == 123
        mock_repo.save.assert_called_once()
        args = mock_repo.save.call_args[0][0]
        assert args.study_id == 1
        assert str(args.meeting_date) == "2024-07-07"
        assert args.monitor == "John Doe"


@pytest.mark.asyncio
async def test_monitoring_list_view_model_load():
    view_model = MonitoringListViewModel()

    mock_data = [
        {
            "monitoring_id": 1,
            "study_id": 1,
            "meeting_date": "2024-01-01",
            "monitor": "M1",
            "comments": "C1",
        },
        {
            "monitoring_id": 2,
            "study_id": 1,
            "meeting_date": "2024-02-01",
            "monitor": "M2",
            "comments": "C2",
        },
    ]

    with patch(
        "src.models.monitoring.MonitoringModel.list", new_callable=AsyncMock
    ) as mock_list:
        mock_list.return_value = [MonitoringDTO.from_dict(m) for m in mock_data]

        await view_model._load_monitoring(1)

        assert len(view_model.monitoring_visits) == 2
        assert view_model.monitoring_visits[0]["monitor"] == "M1"
        assert view_model.monitoring_visits[1]["monitor"] == "M2"
