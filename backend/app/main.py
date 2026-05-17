from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from core import config



app = FastAPI(title="MarketPulse")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)