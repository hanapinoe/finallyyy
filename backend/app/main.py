from fastapi import FastAPI
from app.api import drink_router, user_router, outfit_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(outfit_router.router)
