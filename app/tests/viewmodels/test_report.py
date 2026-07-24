import pytest
from unittest.mock import AsyncMock, patch
from src.viewmodels.report import ReportViewModel

@pytest.mark.asyncio
async def test_report_view_model_load():
    # Setup
    vm = ReportViewModel()
    
    with patch("src.viewmodels.report.ReportRepository") as mock_repo_class:
        mock_repo = mock_repo_class.return_value
        mock_repo.get_study_count = AsyncMock(return_value=5)
        mock_repo.get_patient_count = AsyncMock(return_value=50)
        mock_repo.get_researcher_count = AsyncMock(return_value=10)
        mock_repo.get_visit_count = AsyncMock(return_value=100)
        mock_repo.get_event_count = AsyncMock(return_value=2)
        mock_repo.get_studies = AsyncMock(return_value=[{"study_id": 1, "name": "Study 1"}])
        
        # Action
        await vm.load()
        
        # Verify
        assert vm.study_count == 5
        assert vm.patient_count == 50
        assert vm.studies[1] == "Study 1"

@pytest.mark.asyncio
async def test_report_view_model_load_detail():
    # Setup
    vm = ReportViewModel()
    vm.study_id = 1
    
    with patch("src.viewmodels.report.ReportRepository") as mock_repo_class:
        mock_repo = mock_repo_class.return_value
        mock_repo.get_patient_count_by_study = AsyncMock(return_value=10)
        mock_repo.get_researcher_count_by_study = AsyncMock(return_value=3)
        mock_repo.get_visit_count_by_study = AsyncMock(return_value=20)
        mock_repo.get_event_count_by_study = AsyncMock(return_value=1)
        
        # Action
        await vm.call("load_detail")
        
        # Verify
        assert vm.study_patient_count == 10
        assert vm.study_researcher_count == 3
        assert vm.study_visit_count == 20
        assert vm.study_event_count == 1
        mock_repo.get_patient_count_by_study.assert_called_once_with(1)
