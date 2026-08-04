from unittest.mock import AsyncMock, patch

import pytest
from src.dtos.protocol import ProtocolDTO as Protocol
from src.viewmodels.protocol import ProtocolViewModel
from src.viewmodels.protocol_list import ProtocolListViewModel


@pytest.mark.asyncio
async def test_protocol_view_model_save():
    # Setup
    vm = ProtocolViewModel()
    vm.study_id = 1
    vm.title = "Test Deviation"
    vm.event_date = "2023-01-01"
    vm.description = "Test Description"

    with patch(
        "src.models.protocol.ProtocolModel.save", new_callable=AsyncMock
    ) as mock_save:
        # Action
        await vm.call("save")

        # Verify
        mock_save.assert_called_once()


@pytest.mark.asyncio
async def test_protocol_list_view_model_load():
    # Setup
    vm = ProtocolListViewModel()
    mock_protocols = [
        Protocol(
            protocol_id=1,
            study_id=1,
            title="D1",
            event_date="2023-01-01",
            description="Desc 1",
        ),
        Protocol(
            protocol_id=2,
            study_id=1,
            title="D2",
            event_date="2023-01-02",
            description="Desc 2",
        ),
    ]

    with patch(
        "src.models.protocol.ProtocolModel.list",
        new_callable=AsyncMock,
        return_value=mock_protocols,
    ):
        # Action
        await vm.call("load", study_id=1)

        # Verify
        assert len(vm.protocols) == 2
        assert vm.protocols[0]["title"] == "D1"
        assert vm.protocols[1]["title"] == "D2"


@pytest.mark.asyncio
async def test_protocol_view_model_from_dict():
    # Setup
    data = {
        "protocol_id": 5,
        "study_id": 1,
        "title": "Dict Title",
        "event_date": "2023-05-05",
        "description": "Dict Desc",
    }
    vm = ProtocolViewModel()

    # Action
    vm.from_dict(data)

    # Verify
    assert vm.protocol_id == 5
    assert vm.title == "Dict Title"
    assert vm.event_date == "2023-05-05"
    assert vm.description == "Dict Desc"


@pytest.mark.asyncio
async def test_protocol_view_model_validate():
    # Setup - Invalid (missing title)
    vm = ProtocolViewModel()
    vm.title = ""
    vm.event_date = "2023-01-01"

    # Action
    is_valid = await vm.call("validate")

    # Verify
    assert is_valid is False
    assert vm.is_invalid is True
    assert "Title" in vm.validation
    assert "required" in vm.validation

    # Setup - Invalid (title too short)
    vm.title = "ab"
    is_valid = await vm.call("validate")
    assert is_valid is False
    assert "at least 3 characters" in vm.validation

    # Setup - Invalid (invalid date)
    vm.title = "Valid Title"
    vm.event_date = "not-a-date"
    is_valid = await vm.call("validate")
    assert is_valid is False
    assert "must be a valid date" in vm.validation

    # Setup - Valid
    vm.event_date = "2023-01-01"
    is_valid = await vm.call("validate")
    assert is_valid is True
    assert vm.is_invalid is False
    assert vm.validation == ""


@pytest.mark.asyncio
async def test_protocol_list_deletes_and_reloads_protocols():
    vm = ProtocolListViewModel()
    vm.study_id = 1
    delete = AsyncMock()
    load = AsyncMock()

    with (
        patch.object(vm.model, "delete", delete),
        patch.object(vm, "_load_protocols", load),
    ):
        await vm.call("delete_protocol", protocol_id="9")

    assert vm.protocol_id == 9
    delete.assert_awaited_once_with(9)
    load.assert_awaited_once_with(1)
