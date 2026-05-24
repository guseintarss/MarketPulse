import pytest
from pydantic import ValidationError
from unittest.mock import AsyncMock, MagicMock


class TestProductSchemas:
    def test_product_base_valid(self):
        from app.api_v1.product.schemas import ProductBase
        p = ProductBase(name="Laptop", description="Gaming laptop", price=1500, url="http://example.com")
        assert p.name == "Laptop"
        assert p.price == 1500

    def test_product_base_missing_fields(self):
        from app.api_v1.product.schemas import ProductBase
        with pytest.raises(ValidationError):
            ProductBase()

    def test_product_base_negative_price(self):
        from app.api_v1.product.schemas import ProductBase
        p = ProductBase(name="Test", description="desc", price=-10, url="http://example.com")
        assert p.price == -10

    def test_product_create_inherits(self):
        from app.api_v1.product.schemas import ProductCreate, ProductBase
        assert issubclass(ProductCreate, ProductBase)

    def test_product_update_inherits(self):
        from app.api_v1.product.schemas import ProductUpdate, ProductCreate
        assert issubclass(ProductUpdate, ProductCreate)

    def test_product_update_partial_allows_none(self):
        from app.api_v1.product.schemas import ProductUpdatePatrial
        p = ProductUpdatePatrial()
        assert p.name is None
        assert p.description is None
        assert p.price is None
        assert p.url is None

    def test_product_update_partial_partial(self):
        from app.api_v1.product.schemas import ProductUpdatePatrial
        p = ProductUpdatePatrial(name="Updated")
        assert p.name == "Updated"
        assert p.description is None

    def test_product_response_schema(self):
        from app.api_v1.product.schemas import Product
        p = Product(id=1, name="Laptop", description="Desc", price=1000, url="http://example.com")
        assert p.id == 1
        assert p.model_config.get("from_attributes") is True


class TestProductCRUD:
    @pytest.mark.asyncio
    async def test_get_products_empty(self, async_session):
        from app.api_v1.product.crud import get_products
        products = await get_products(session=async_session)
        assert products == []

    @pytest.mark.asyncio
    async def test_create_and_get_product(self, async_session):
        from app.api_v1.product.crud import create_product, get_product
        from app.api_v1.product.schemas import ProductCreate

        product_in = ProductCreate(name="Laptop", description="Gaming", price=1500, url="http://example.com")
        created = await create_product(session=async_session, product_in=product_in)
        assert created.id is not None
        assert created.name == "Laptop"
        assert created.price == 1500

        fetched = await get_product(session=async_session, product_id=created.id)
        assert fetched is not None
        assert fetched.name == "Laptop"

    @pytest.mark.asyncio
    async def test_get_product_not_found(self, async_session):
        from app.api_v1.product.crud import get_product
        result = await get_product(session=async_session, product_id=999)
        assert result is None

    @pytest.mark.asyncio
    async def test_create_multiple_products(self, async_session):
        from app.api_v1.product.crud import create_product, get_products
        from app.api_v1.product.schemas import ProductCreate

        for i in range(3):
            await create_product(
                session=async_session,
                product_in=ProductCreate(
                    name=f"Product {i}", description=f"Desc {i}",
                    price=100 * i, url=f"http://example.com/{i}",
                ),
            )

        products = await get_products(session=async_session)
        assert len(products) == 3

    @pytest.mark.asyncio
    async def test_update_product(self, async_session):
        from app.api_v1.product.crud import create_product, update_product
        from app.api_v1.product.schemas import ProductCreate, ProductUpdate

        created = await create_product(
            session=async_session,
            product_in=ProductCreate(name="Old", description="Old desc", price=100, url="http://example.com"),
        )
        updated = await update_product(
            session=async_session,
            product=created,
            product_update=ProductUpdate(name="New", description="New desc", price=200, url="http://new.com"),
        )
        assert updated.name == "New"
        assert updated.price == 200
        assert updated.url == "http://new.com"

    @pytest.mark.asyncio
    async def test_update_product_partial(self, async_session):
        from app.api_v1.product.crud import create_product, update_product
        from app.api_v1.product.schemas import ProductCreate, ProductUpdatePatrial

        created = await create_product(
            session=async_session,
            product_in=ProductCreate(name="Original", description="Desc", price=100, url="http://example.com"),
        )
        updated = await update_product(
            session=async_session,
            product=created,
            product_update=ProductUpdatePatrial(price=999),
            partial=True,
        )
        assert updated.name == "Original"
        assert updated.price == 999
        assert updated.description == "Desc"

    @pytest.mark.asyncio
    async def test_delete_product(self, async_session):
        from app.api_v1.product.crud import create_product, delete_product, get_product
        from app.api_v1.product.schemas import ProductCreate

        created = await create_product(
            session=async_session,
            product_in=ProductCreate(name="ToDelete", description="Desc", price=50, url="http://example.com"),
        )
        await delete_product(session=async_session, product=created)

        fetched = await get_product(session=async_session, product_id=created.id)
        assert fetched is None


class TestProductDependencies:
    @pytest.mark.asyncio
    async def test_product_by_id_found(self, async_session):
        from app.api_v1.product.crud import create_product
        from app.api_v1.product.dependencies import product_by_id
        from app.api_v1.product.schemas import ProductCreate

        created = await create_product(
            session=async_session,
            product_in=ProductCreate(name="Test", description="Desc", price=100, url="http://example.com"),
        )
        result = await product_by_id(product_id=created.id, session=async_session)
        assert result is not None
        assert result.id == created.id

    @pytest.mark.asyncio
    async def test_product_by_id_not_found(self, async_session):
        from app.api_v1.product.dependencies import product_by_id
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            await product_by_id(product_id=999, session=async_session)
        assert exc_info.value.status_code == 404
        assert "999" in exc_info.value.detail


class TestProductViews:
    def test_get_products_empty(self, client):
        response = client.get("/api/v1/products/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_and_get_product(self, client):
        create_resp = client.post("/api/v1/products/", json={
            "name": "Test Product",
            "description": "A test product",
            "price": 100,
            "url": "http://example.com/product",
        })
        assert create_resp.status_code == 201
        data = create_resp.json()
        assert data["name"] == "Test Product"
        assert data["price"] == 100
        assert data["id"] is not None

        product_id = data["id"]
        get_resp = client.get(f"/api/v1/products/{product_id}/")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "Test Product"

    def test_create_product_missing_fields(self, client):
        response = client.post("/api/v1/products/", json={})
        assert response.status_code == 422

    def test_get_product_not_found(self, client):
        response = client.get("/api/v1/products/99999/")
        assert response.status_code == 404

    def test_get_product_invalid_id(self, client):
        response = client.get("/api/v1/products/abc/")
        assert response.status_code == 422

    def test_update_product(self, client):
        create_resp = client.post("/api/v1/products/", json={
            "name": "Original", "description": "Original desc",
            "price": 100, "url": "http://example.com",
        })
        product_id = create_resp.json()["id"]

        update_resp = client.put(f"/api/v1/products/{product_id}/", json={
            "name": "Updated", "description": "Updated desc",
            "price": 200, "url": "http://updated.com",
        })
        assert update_resp.status_code == 200
        assert update_resp.json()["name"] == "Updated"
        assert update_resp.json()["price"] == 200

    def test_update_product_not_found(self, client):
        response = client.put("/api/v1/products/99999/", json={
            "name": "Updated", "description": "Desc", "price": 200, "url": "http://example.com",
        })
        assert response.status_code == 404

    def test_patch_product(self, client):
        create_resp = client.post("/api/v1/products/", json={
            "name": "Original", "description": "Desc",
            "price": 100, "url": "http://example.com",
        })
        product_id = create_resp.json()["id"]

        patch_resp = client.patch(f"/api/v1/products/{product_id}/", json={"price": 150})
        assert patch_resp.status_code == 200
        assert patch_resp.json()["price"] == 150
        assert patch_resp.json()["name"] == "Original"

    def test_patch_product_not_found(self, client):
        response = client.patch("/api/v1/products/99999/", json={"price": 150})
        assert response.status_code == 404

    def test_delete_product(self, client):
        create_resp = client.post("/api/v1/products/", json={
            "name": "ToDelete", "description": "Desc",
            "price": 50, "url": "http://example.com",
        })
        product_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/api/v1/products/{product_id}/")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/api/v1/products/{product_id}/")
        assert get_resp.status_code == 404

    def test_delete_product_not_found(self, client):
        response = client.delete("/api/v1/products/99999/")
        assert response.status_code == 404

    def test_list_products_after_create(self, client):
        client.post("/api/v1/products/", json={
            "name": "A", "description": "Desc A", "price": 10, "url": "http://a.com",
        })
        client.post("/api/v1/products/", json={
            "name": "B", "description": "Desc B", "price": 20, "url": "http://b.com",
        })

        response = client.get("/api/v1/products/")
        assert response.status_code == 200
        assert len(response.json()) == 2
