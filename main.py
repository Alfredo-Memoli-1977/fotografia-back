from typing import Literal
from fastapi import FastAPI,Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from photos.routes import router as photos_router
from users.routes import router as users_router
from auth.routes import router as auth_router

app = FastAPI()

app.include_router(photos_router)
app.include_router(users_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://192.168.1.135:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")




