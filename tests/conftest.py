import sys
import pytest
import pytest_asyncio
from pathlib import Path
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
BACKEND_DIR = PROJECT_DIR / "backend"
BACKEND_APP_DIR = BACKEND_DIR / "app"

for p in [str(BACKEND_DIR), str(BACKEND_APP_DIR), str(PROJECT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.models import Base


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def _make_engine():
    return create_async_engine(
        "sqlite+aiosqlite://",
        echo=False,
        connect_args={"check_same_thread": False},
    )


async def _init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def async_session():
    engine = _make_engine()
    await _init_db(engine)
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    async with session_factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture
def client():
    import asyncio
    from backend.main import app

    test_engine = _make_engine()
    asyncio.run(_init_db(test_engine))

    async def override_session_dependency():
        session_factory = async_sessionmaker(
            bind=test_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        async with session_factory() as session:
            yield session

    from app.core.models import db_helper

    app.dependency_overrides[db_helper.session_dependency] = override_session_dependency

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    asyncio.run(test_engine.dispose())


@pytest.fixture
def auth_credentials():
    return {"username": "Bob", "password": "qwerty"}
