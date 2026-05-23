from fastapi import APIRouter
from .auth.views import router as auth_router
from .auth.jwt_auth import router as auth_jwt_router
from .product.views import router as products_router

router = APIRouter()
router.include_router(router=products_router, prefix="/products")
router.include_router(router=auth_router)
router.include_router(router=auth_jwt_router)
