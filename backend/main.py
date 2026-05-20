from typing import Annotated

import uvicorn
from app.users.views import router as user_router 
from fastapi import Body
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import EmailStr

app = FastAPI()
app.include_router(user_router)



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
