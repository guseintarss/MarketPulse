import pytest
from datetime import datetime, timedelta


class TestHashPassword:
    def test_hash_password_returns_bytes(self):
        from auth.utils import hash_password
        hashed = hash_password("testpassword")
        assert isinstance(hashed, bytes)
        assert hashed != b""

    def test_hash_password_differs_from_original(self):
        from auth.utils import hash_password
        hashed = hash_password("testpassword")
        assert hashed != b"testpassword"

    def test_hash_is_different_each_time(self):
        from auth.utils import hash_password
        h1 = hash_password("testpassword")
        h2 = hash_password("testpassword")
        assert h1 != h2


class TestValidatePassword:
    def test_validate_correct_password(self):
        from auth.utils import hash_password, validate_password
        password = "secret123"
        hashed = hash_password(password)
        assert validate_password(password, hashed) is True

    def test_validate_incorrect_password(self):
        from auth.utils import hash_password, validate_password
        hashed = hash_password("correctpassword")
        assert validate_password("wrongpassword", hashed) is False

    def test_validate_empty_password(self):
        from auth.utils import hash_password, validate_password
        hashed = hash_password("somepassword")
        assert validate_password("", hashed) is False


class TestEncodeJWT:
    def test_encode_returns_string(self):
        from auth.utils import encode_jwt
        payload = {"sub": "testuser", "username": "testuser"}
        token = encode_jwt(payload)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_encode_with_custom_expiry(self):
        from auth.utils import encode_jwt
        payload = {"sub": "testuser"}
        token = encode_jwt(payload, expire_minutes=60)
        assert isinstance(token, str)

    def test_encode_with_timedelta(self):
        from auth.utils import encode_jwt
        payload = {"sub": "testuser"}
        token = encode_jwt(payload, expire_timedelta=timedelta(hours=1))
        assert isinstance(token, str)


class TestDecodeJWT:
    def test_decode_valid_token(self):
        from auth.utils import encode_jwt, decode_jwt
        payload = {"sub": "testuser", "username": "testuser", "email": "test@example.com"}
        token = encode_jwt(payload)
        decoded = decode_jwt(token)
        assert decoded["sub"] == "testuser"
        assert decoded["username"] == "testuser"
        assert decoded["email"] == "test@example.com"

    def test_decode_contains_exp_and_iat(self):
        from auth.utils import encode_jwt, decode_jwt
        payload = {"sub": "testuser"}
        token = encode_jwt(payload)
        decoded = decode_jwt(token)
        assert "exp" in decoded
        assert "iat" in decoded

    def test_decode_expired_token_raises_error(self):
        from auth.utils import encode_jwt, decode_jwt
        import jwt as pyjwt
        payload = {"sub": "testuser"}
        token = encode_jwt(payload, expire_minutes=-1)
        with pytest.raises(pyjwt.ExpiredSignatureError):
            decode_jwt(token)

    def test_decode_invalid_token_raises_error(self):
        from auth.utils import decode_jwt
        import jwt as pyjwt
        with pytest.raises((pyjwt.DecodeError, pyjwt.InvalidSignatureError, pyjwt.ExpiredSignatureError)):
            decode_jwt("invalid.token.here")


class TestEncodeDecodeRoundTrip:
    def test_round_trip_preserves_data(self):
        from auth.utils import encode_jwt, decode_jwt
        original = {"sub": "john", "username": "john_doe", "email": "john@example.com"}
        token = encode_jwt(original)
        decoded = decode_jwt(token)
        for key in original:
            assert decoded[key] == original[key]
