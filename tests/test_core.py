import pytest
from pydantic import ValidationError


class TestSettings:
    def test_settings_defaults(self):
        from app.core.config import Settings
        s = Settings()
        assert s.api_v1_prefix == "/api/v1"
        assert s.db.url == "postgresql+asyncpg://postgres:postgres@localhost/postgres"
        assert s.db.echo is True
        assert s.auth_jwt.algoritm == "RS256"
        assert s.auth_jwt.access_token_expire_minutes == 3

    def test_settings_custom_env(self, monkeypatch):
        monkeypatch.setenv("API_V1_PREFIX", "/api/test")
        from app.core.config import Settings
        s = Settings()
        assert s.api_v1_prefix == "/api/test"

    def test_settings_db_nested_env_not_supported(self, monkeypatch):
        monkeypatch.setenv("DB__URL", "sqlite+aiosqlite:///test.db")
        from app.core.config import Settings
        s = Settings()
        assert s.db.url == "postgresql+asyncpg://postgres:postgres@localhost/postgres"

    def test_settings_auth_jwt_nested_env_not_supported(self, monkeypatch):
        monkeypatch.setenv("AUTH_JWT__ACCESS_TOKEN_EXPIRE_MINUTES", "10")
        from app.core.config import Settings
        s = Settings()
        assert s.auth_jwt.access_token_expire_minutes == 3

    def test_cert_paths_exist(self):
        from app.core.config import settings
        assert settings.auth_jwt.private_key_path.exists()
        assert settings.auth_jwt.public_key_path.exists()


class TestBaseModel:
    def test_tablename_convention(self):
        from app.core.models.base import Base
        assert Base.__abstract__ is True

    def test_tablename_generated(self):
        from app.core.models.product import Product
        assert Product.__tablename__ == "product"

    def test_base_id_column(self):
        from app.core.models.base import Base
        assert hasattr(Base, "id")


class TestUserModel:
    def test_user_creation(self):
        from app.core.models.user import User
        u = User(username="testuser")
        assert u.username == "testuser"
        assert str(u) == "User(id=None, username='testuser')"
        assert repr(u) == "User(id=None, username='testuser')"

    def test_user_defaults(self):
        from app.core.models.user import User
        u = User()
        assert u.username is None
        assert u.id is None


class TestProfileModel:
    def test_profile_creation(self):
        from app.core.models.profile import Profile
        p = Profile(firstname="John", lastname="Doe", age=30)
        assert p.firstname == "John"
        assert p.lastname == "Doe"
        assert p.age == 30

    def test_profile_defaults(self):
        from app.core.models.profile import Profile
        p = Profile()
        assert p.firstname is None
        assert p.lastname is None
        assert p.age is None
        assert p.user_id is None

    def test_profile_user_relation(self):
        from app.core.models.profile import Profile
        assert Profile._user_id_unique is True
        assert Profile._user_back_populates == "profile"


class TestProductModel:
    def test_product_creation(self):
        from app.core.models.product import Product
        p = Product(name="Test", description="Desc", price=100, url="http://example.com")
        assert p.name == "Test"
        assert p.description == "Desc"
        assert p.price == 100
        assert p.url == "http://example.com"

    def test_product_defaults(self):
        from app.core.models.product import Product
        p = Product()
        assert p.id is None

    def test_product_tablename(self):
        from app.core.models.product import Product
        assert Product.__tablename__ == "product"


class TestUserRelationMixin:
    def test_mixin_defaults(self):
        from app.core.models.mixin import UserRelationMixin
        assert UserRelationMixin._user_id_nullable is False
        assert UserRelationMixin._user_id_unique is False
        assert UserRelationMixin._user_back_populates is None


class TestDatabaseHelper:
    def test_init_creates_engine(self):
        from app.core.models.db_helper import DatabaseHelper
        helper = DatabaseHelper(url="sqlite+aiosqlite:///:memory:", echo=False)
        assert helper.engine is not None
        assert helper.session_factory is not None

    def test_session_dependency(self):
        from app.core.models.db_helper import DatabaseHelper
        helper = DatabaseHelper(url="sqlite+aiosqlite:///:memory:", echo=False)
        assert helper.session_factory is not None

    @pytest.mark.asyncio
    async def test_session_dependency_yields_session(self):
        from app.core.models.db_helper import DatabaseHelper
        helper = DatabaseHelper(url="sqlite+aiosqlite:///:memory:", echo=False)
        async for session in helper.session_dependency():
            assert session is not None
            break

    def test_get_scopd_session(self):
        from app.core.models.db_helper import DatabaseHelper
        helper = DatabaseHelper(url="sqlite+aiosqlite:///:memory:", echo=False)
        scoped = helper.get_scopd_session()
        assert scoped is not None


class TestModuleExports:
    def test_all_exports(self):
        from app.core.models import Base, Product, User, DatabaseHelper, db_helper, Profile
        assert Base is not None
        assert Product is not None
        assert User is not None
        assert DatabaseHelper is not None
        assert db_helper is not None
        assert Profile is not None
