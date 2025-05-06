from fastapi import FastAPI
from app.api.routes import router as search_router

app = FastAPI()

app.include_router(search_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Hello, Social Search!"}