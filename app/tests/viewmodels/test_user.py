import pytest
from unittest.mock import AsyncMock, patch
from src.viewmodels.user import UserViewModel
from src.viewmodels.user_list import UserListViewModel
from src.dtos.user import UserDTO


@pytest.mark.asyncio
async def test_user_list_view_model_load():
    # Setup
    vm = UserListViewModel()
    mock_users = [
        UserDTO(
            user_id=1,
            user_name="user1",
            pass_hash="h1",
            user_role="User",
            created_by="admin",
            updated_by="admin",
        ),
        UserDTO(
            user_id=2,
            user_name="user2",
            pass_hash="h2",
            user_role="Admin",
            created_by="admin",
            updated_by="admin",
        ),
    ]

    with patch(
        "src.models.user.UserModel.list",
        new_callable=AsyncMock,
        return_value=mock_users,
    ):
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

    with (
        patch(
            "src.models.user.UserModel.delete", new_callable=AsyncMock
        ) as mock_delete,
        patch(
            "src.models.user.UserModel.list", new_callable=AsyncMock, return_value=[]
        ),
    ):
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


@pytest.mark.asyncio
async def test_user_view_model_save():
    # Setup
    vm = UserViewModel()
    vm.user_name = "new_user"
    vm.password_1 = "secret"
    vm.user_role = "User"

    with patch("src.models.user.UserModel.repo") as mock_repo:
        mock_repo.save = AsyncMock(return_value={"user_id": 999})

        # Action
        await vm.save()

        # Verify
        assert vm.user_id == 999
        assert vm.pass_hash != ""
        mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_user_view_model_load():
    # Setup
    vm = UserViewModel()
    mock_user = UserDTO(
        user_id=999,
        user_name="loaded_user",
        pass_hash="some_hash",
        user_role="Admin",
        created_by="admin",
        updated_by="admin",
    )

    with patch(
        "src.models.user.UserModel.load", new_callable=AsyncMock, return_value=mock_user
    ):
        # Action
        await vm.call("load", user_id=999)

        # Verify
        assert vm.user_id == 999
        assert vm.user_name == "loaded_user"
        assert vm.user_role == "Admin"
