import base64
import pytest


class TestBasicAuth:
    def _basic_auth_header(self, username: str, password: str) -> dict:
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def test_basic_auth_valid_credentials(self, client):
        response = client.get(
            "/api/v1/auth/basic-auth",
            headers=self._basic_auth_header("admin", "admin"),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "hi1"
        assert data["username"] == "admin"
        assert data["password"] == "admin"

    def test_basic_auth_no_credentials(self, client):
        response = client.get("/api/v1/auth/basic-auth")
        assert response.status_code == 401

    def test_basic_auth_empty_credentials(self, client):
        response = client.get(
            "/api/v1/auth/basic-auth",
            headers=self._basic_auth_header("", ""),
        )
        assert response.status_code == 200
        assert response.json()["username"] == ""
        assert response.json()["password"] == ""


class TestJWTAuth:
    def test_jwt_login_valid(self, client, auth_credentials):
        response = client.post("/api/v1/jwt/login", data=auth_credentials)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "Bearer"

    def test_jwt_login_invalid_username(self, client):
        response = client.post("/api/v1/jwt/login", data={
            "username": "nonexistent",
            "password": "qwerty",
        })
        assert response.status_code == 401

    def test_jwt_login_invalid_password(self, client):
        response = client.post("/api/v1/jwt/login", data={
            "username": "Bob",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_jwt_login_empty_password(self, client):
        response = client.post("/api/v1/jwt/login", data={
            "username": "Bob",
            "password": "",
        })
        assert response.status_code in (401, 422)

    def test_jwt_login_missing_fields(self, client):
        response = client.post("/api/v1/jwt/login")
        assert response.status_code == 422

    def test_jwt_token_format(self, client, auth_credentials):
        response = client.post("/api/v1/jwt/login", data=auth_credentials)
        token = response.json()["access_token"]
        parts = token.split(".")
        assert len(parts) == 3

    def test_jwt_token_decodes(self, client, auth_credentials):
        from auth.utils import decode_jwt
        response = client.post("/api/v1/jwt/login", data=auth_credentials)
        token = response.json()["access_token"]
        decoded = decode_jwt(token)
        assert decoded["sub"] == "Bob"
        assert decoded["username"] == "Bob"

    def test_jwt_users_me_missing_params(self, client):
        response = client.get("/api/v1/jwt/users/me/")
        assert response.status_code == 422
