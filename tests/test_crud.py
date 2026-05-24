import pytest
from unittest.mock import AsyncMock, MagicMock


class TestUserCrud:
    @pytest.mark.asyncio
    async def test_create_user(self):
        from crud import create_user
        mock_session = AsyncMock()
        result = await create_user(session=mock_session, username="testuser")
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()
        assert result.username == "testuser"

    @pytest.mark.asyncio
    async def test_get_user_by_username_found(self):
        from crud import get_user_by_username
        mock_session = AsyncMock()
        mock_user = MagicMock()
        mock_session.scalar = AsyncMock(return_value=mock_user)
        result = await get_user_by_username(session=mock_session, username="Bob")
        assert result is mock_user

    @pytest.mark.asyncio
    async def test_get_user_by_username_not_found(self):
        from crud import get_user_by_username
        mock_session = AsyncMock()
        mock_session.scalar = AsyncMock(return_value=None)
        result = await get_user_by_username(session=mock_session, username="Nobody")
        assert result is None


class TestProfileCrud:
    @pytest.mark.asyncio
    async def test_create_user_profile(self):
        from crud import create_user_profile
        mock_session = AsyncMock()
        result = await create_user_profile(
            session=mock_session, user_id=1,
            firstname="John", lastname="Doe",
        )
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()
        assert result.firstname == "John"
        assert result.lastname == "Doe"
        assert result.user_id == 1

    @pytest.mark.asyncio
    async def test_create_user_profile_defaults(self):
        from crud import create_user_profile
        mock_session = AsyncMock()
        result = await create_user_profile(session=mock_session, user_id=1)
        assert result.firstname is None
        assert result.lastname is None
