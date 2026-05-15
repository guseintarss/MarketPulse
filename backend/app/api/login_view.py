from fastapi import FastAPI
from authx import AuthX, AuthXConfig


app = FastAPI()
config = AuthXConfig()

config.JWT_SECRET_KEY = "fslrifna23rr203fjfja)_fe239jfew>?vkpwqwkHomePassword"
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)


@app.post("/login")
def login():
    pass

@app.post("/protected")
def protected():
    pass