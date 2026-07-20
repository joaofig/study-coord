import pytest
from unittest.mock import AsyncMock, patch
from src.viewmodels.user_list import UserListViewModel
from src.dtos.user import UserDTO

@pytest.mark.asyncio
async def test_user_list_view_model_load():
    # Setup
    vm = UserListViewModel()
    mock_users = [
        UserDTO(user_id=1, user_name="user1", pass_hash="h1", role="User", created_by="admin", updated_by="admin"),
        UserDTO(user_id=2, user_name="user2", pass_hash="h2", role="Admin", created_by="admin", updated_by="admin"),
    ]
    
    with patch("src.models.user.UserModel.list", new_callable=AsyncMock, return_value=mock_users):
        # Action
        await vm.call("load")
        
        # Verify
        assert len(vm.users) == 2
        assert vm.users[0].user_name == "user1"
        assert vm.users[1].user_name == "user2"

@pytest.mark.asyncio
async def test_user_list_view_model_delete():
    # Setup
    vm = UserListViewModel()
    
    with patch("src.models.user.UserModel.delete", new_callable=AsyncMock) as mock_delete, \
         patch("src.models.user.UserModel.list", new_callable=AsyncMock, return_value=[]):
        # Action
        await vm.call("delete", user_id=1)
        
        # Verify
        mock_delete.assert_called_once_with(user_id=1)

@pytest.mark.asyncio
async def test_user_list_view_model_selected():
    # Setup
    vm = UserListViewModel()
    
    # Action
    await vm.call("user_selected", user_id=123)
    
    # Verify
    assert vm.selected_id == 123
