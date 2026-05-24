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
    def _register_user(
        self, client, username="testuser", password="testpass", email="test@example.com"
    ):
        return client.post(
            "/api/v1/jwt/register",
            json={
                "username": username,
                "password": password,
                "email": email,
            },
        )

    def test_register_user(self, client):
        resp = self._register_user(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "Bearer"

    def test_register_duplicate_username(self, client):
        self._register_user(client, username="alice")
        resp = self._register_user(client, username="alice")
        assert resp.status_code == 409

    def test_register_invalid_data(self, client):
        resp = client.post(
            "/api/v1/jwt/register",
            json={
                "username": "ab",
                "password": "12",
                "email": "not-email",
            },
        )
        assert resp.status_code == 422

    def test_jwt_login_valid(self, client):
        self._register_user(
            client, username="bob", password="qwerty", email="bob@test.com"
        )
        resp = client.post(
            "/api/v1/jwt/login",
            data={
                "username": "bob",
                "password": "qwerty",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "Bearer"

    def test_jwt_login_invalid_username(self, client):
        resp = client.post(
            "/api/v1/jwt/login",
            data={
                "username": "nonexistent",
                "password": "qwerty",
            },
        )
        assert resp.status_code == 401

    def test_jwt_login_invalid_password(self, client):
        self._register_user(client, username="charlie", password="secret")
        resp = client.post(
            "/api/v1/jwt/login",
            data={
                "username": "charlie",
                "password": "wrongpassword",
            },
        )
        assert resp.status_code == 401

    def test_jwt_login_missing_fields(self, client):
        resp = client.post("/api/v1/jwt/login")
        assert resp.status_code == 422

    def test_jwt_token_format(self, client):
        self._register_user(client, username="tokenuser", password="testpass")
        resp = client.post(
            "/api/v1/jwt/login",
            data={
                "username": "tokenuser",
                "password": "testpass",
            },
        )
        token = resp.json()["access_token"]
        parts = token.split(".")
        assert len(parts) == 3

    def test_jwt_token_decodes(self, client):
        self._register_user(
            client, username="decodeuser", password="testpass", email="decode@test.com"
        )
        resp = client.post(
            "/api/v1/jwt/login",
            data={
                "username": "decodeuser",
                "password": "testpass",
            },
        )
        from auth.utils import decode_jwt

        token = resp.json()["access_token"]
        decoded = decode_jwt(token)
        assert decoded["sub"] == "decodeuser"

    def test_jwt_users_me_authenticated(self, client):
        self._register_user(client, username="meuser", password="testpass")
        login_resp = client.post(
            "/api/v1/jwt/login",
            data={
                "username": "meuser",
                "password": "testpass",
            },
        )
        token = login_resp.json()["access_token"]
        resp = client.get(
            "/api/v1/jwt/users/me/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["username"] == "meuser"

    def test_jwt_users_me_unauthenticated(self, client):
        resp = client.get("/api/v1/jwt/users/me/")
        assert resp.status_code in (401, 403)

    def test_jwt_users_me_invalid_token(self, client):
        resp = client.get(
            "/api/v1/jwt/users/me/",
            headers={
                "Authorization": "Bearer invalidtoken",
            },
        )
        assert resp.status_code == 401
