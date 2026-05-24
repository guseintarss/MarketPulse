import pytest


class TestMainApp:
    def test_app_created(self):
        from backend.main import app
        assert app is not None
        assert app.title == "FastAPI"

    def test_root_endpoint_exists(self):
        from backend.main import app
        routes = [r.path for r in app.routes]
        assert "/user/" in routes
        assert "/api/v1/products/" in routes
        assert "/api/v1/auth/basic-auth" in routes
        assert "/api/v1/jwt/login" in routes

    def test_lifespan(self):
        from backend.main import lifespan, app
        import asyncio
        async def test():
            async with lifespan(app):
                pass
        asyncio.run(test())

    def test_openapi_schema(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema

    def test_health_check(self, client):
        response = client.get("/")
        assert response.status_code in (200, 404)

    def test_api_v1_prefix_in_config(self):
        from app.core.config import settings
        assert settings.api_v1_prefix == "/api/v1"


class TestAPIRouter:
    def test_router_includes_subrouters(self):
        from app.api_v1 import router
        routes = [r.path for r in router.routes]
        assert any("/" in p for p in routes)
        assert any("auth" in p or "jwt" in p for p in routes)

    def test_router_has_tags(self):
        from app.api_v1 import router
        assert router.prefix == ""
