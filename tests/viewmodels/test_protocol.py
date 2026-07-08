import pytest
from unittest.mock import AsyncMock, patch
from viewmodels.ProtocolViewModel import ProtocolViewModel
from viewmodels.ProtocolListViewModel import ProtocolListViewModel
from models.protocol import Protocol

@pytest.mark.asyncio
async def test_protocol_view_model_save():
    # Setup
    vm = ProtocolViewModel()
    vm.study_id = 1
    vm.title = "Test Deviation"
    vm.date = "2023-01-01"
    vm.description = "Test Description"
    
    with patch("src.models.protocol.Protocol.save", new_callable=AsyncMock) as mock_save:
        # Action
        await vm.call("save")
        
        # Verify
        mock_save.assert_called_once()

@pytest.mark.asyncio
async def test_protocol_list_view_model_load():
    # Setup
    vm = ProtocolListViewModel()
    mock_protocols = [
        Protocol(id=1, study_id=1, title="D1", date="2023-01-01", description="Desc 1"),
        Protocol(id=2, study_id=1, title="D2", date="2023-01-02", description="Desc 2"),
    ]
    
    with patch("src.models.protocol.ProtocolList.load_from_study", return_value=mock_protocols):
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
        "id": 5,
        "study_id": 1,
        "title": "Dict Title",
        "date": "2023-05-05",
        "description": "Dict Desc"
    }
    vm = ProtocolViewModel()
    
    # Action
    vm.from_dict(data)
    
    # Verify
    assert vm.id == 5
    assert vm.title == "Dict Title"
    assert vm.date == "2023-05-05"
    assert vm.description == "Dict Desc"
