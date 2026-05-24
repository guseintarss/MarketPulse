import pytest
from pydantic import ValidationError


class TestCreateUserSchema:
    def test_valid_user(self):
        from app.users.schemas import CreateUser
        user = CreateUser(username="testuser", email="test@example.com")
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_username_too_short(self):
        from app.users.schemas import CreateUser
        with pytest.raises(ValidationError):
            CreateUser(username="ab", email="test@example.com")

    def test_username_too_long(self):
        from app.users.schemas import CreateUser
        with pytest.raises(ValidationError):
            CreateUser(username="a" * 51, email="test@example.com")

    def test_invalid_email(self):
        from app.users.schemas import CreateUser
        with pytest.raises(ValidationError):
            CreateUser(username="testuser", email="not-an-email")

    def test_empty_username(self):
        from app.users.schemas import CreateUser
        with pytest.raises(ValidationError):
            CreateUser(username="", email="test@example.com")

    def test_missing_fields(self):
        from app.users.schemas import CreateUser
        with pytest.raises(ValidationError):
            CreateUser()


class TestUserSchema:
    def test_valid_user_schema(self):
        from app.users.schemas import UserShema
        user = UserShema(
            username="Bob",
            password=b"hashedpassword",
            email="bob@example.com",
            is_active=True,
        )
        assert user.username == "Bob"
        assert user.password == b"hashedpassword"
        assert user.email == "bob@example.com"
        assert user.is_active is True

    def test_user_schema_defaults(self):
        from app.users.schemas import UserShema
        user = UserShema(username="Bob", password=b"pass")
        assert user.email is None
        assert user.is_active is True

    def test_user_schema_strict_types(self):
        from app.users.schemas import UserShema
        with pytest.raises(ValidationError):
            UserShema(username="Bob", password="not-bytes")

    def test_user_schema_empty_username_valid_in_strict_mode(self):
        from app.users.schemas import UserShema
        user = UserShema(username="", password=b"pass")
        assert user.username == ""


class TestCreateUserCRUD:
    def test_create_user(self):
        from app.users.crud import create_user
        from app.users.schemas import CreateUser
        user_in = CreateUser(username="john", email="john@example.com")
        result = create_user(user_in)
        assert result["success"] is True
        assert result["user"]["username"] == "john"
        assert result["user"]["email"] == "john@example.com"

    def test_create_user_includes_all_fields(self):
        from app.users.crud import create_user
        from app.users.schemas import CreateUser
        user_in = CreateUser(username="alice", email="alice@example.com")
        result = create_user(user_in)
        assert set(result["user"].keys()) == {"username", "email"}


class TestUserViews:
    def test_create_user_endpoint(self, client):
        response = client.post("/user/", json={
            "username": "testuser",
            "email": "test@example.com",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["username"] == "testuser"
        assert data["user"]["email"] == "test@example.com"

    def test_create_user_invalid_email(self, client):
        response = client.post("/user/", json={
            "username": "testuser",
            "email": "invalid",
        })
        assert response.status_code == 422

    def test_create_user_short_username(self, client):
        response = client.post("/user/", json={
            "username": "ab",
            "email": "test@example.com",
        })
        assert response.status_code == 422

    def test_create_user_missing_fields(self, client):
        response = client.post("/user/", json={})
        assert response.status_code == 422
