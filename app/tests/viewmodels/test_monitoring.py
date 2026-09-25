from unittest.mock import AsyncMock, patch

import pytest
from src.dtos.monitorization import MonitorizationDTO
from src.viewmodels.study.monitorization import MonitorizationViewModel
from src.viewmodels.study.monitorization_list import MonitoringListViewModel


@pytest.mark.asyncio
async def test_monitoring_view_model_validate():
    # Setup - Invalid (missing monitor)
    vm = MonitorizationViewModel()
    vm.meeting_date = "2024-07-07"
    vm.monitor = ""

    # Action
    is_valid = await vm.call("validate")

    # Verify
    assert is_valid is False
    assert vm.is_invalid is True
    assert "Monitor" in vm.validation

    # Setup - Invalid (invalid date)
    vm.monitor = "John Doe"
    vm.meeting_date = "not-a-date"
    is_valid = await vm.call("validate")
    assert is_valid is False
    assert "valid date" in vm.validation

    # Setup - Valid
    vm.meeting_date = "2024-07-07"
    is_valid = await vm.call("validate")
    assert is_valid is True
    assert vm.is_invalid is False
    assert vm.validation == ""


@pytest.mark.asyncio
async def test_monitoring_list_selects_and_deletes_monitoring_visit():
    view_model = MonitoringListViewModel()
    view_model.monitorization_visits.replace([{"monitoring_id": 7, "monitor": "M1"}])
    delete = AsyncMock()

    with patch.object(view_model.model, "delete", delete):
        await view_model.call("select", monitoring_id=7)
        await view_model.call("delete", monitoring_id=7)

    assert view_model.selected_id == 7
    delete.assert_awaited_once_with(7)
    assert view_model.monitorization_visits == []
