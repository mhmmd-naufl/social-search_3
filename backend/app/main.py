from fastapi import FastAPI
from app import search
from app.api import tiktok

app = FastAPI()

app.include_router(tiktok.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Hello, Social Search!"}